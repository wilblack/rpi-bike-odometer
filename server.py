import tornado.ioloop
import tornado.web
import tornado.websocket

import time, threading, time, os
from random import randint
from math import pi



PATH = os.path.dirname(os.path.abspath(__file__))

try:
   import RPi.GPIO as io
except:
    print "Could not import RPi.GPIO. Are you on a Raspberry Pi?"

        
io.setmode(io.BCM)
         
pir_pin = 18
door_pin = 23
        
io.setup(pir_pin, io.IN)         # activate input
io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with Pull
print "Sensors intialized correctly"

clients = []


class OdometerThread (threading.Thread):

    def __init__(self, socket):
        super(OdometerThread, self).__init__()
        self.stoprequest = threading.Event()
        self.socket = socket
        self.DT = 1

    def run(self):
        print "Starting Odometer Thread"

        wheel_circumference = 0.5 * 2 * pi   # wheel diameter in meters
        count = 0
        then = time.time()
        flag = False
        spd = 0.0
        dt = 0.0
        total_dist = 0.0
        while not self.stoprequest.isSet():

            if io.input(door_pin):
                if flag:
                    flag = False
                else:
                    if not flag:
                        flag = True
                        count = count + 1
                        now = time.time()
                        dt = now - then
                        total_dist = total_dist + wheel_circumference
                        spd = wheel_circumference / dt
                        text = "count: %s speed: %.1fm/s  dist: %.1fm \r" % (count, spd, total_dist)
                        print text
                        self.socket.write_message({'text': text})
                        then = now
            if self.stoprequest.isSet():
                print "******** STOP IT ************"


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class SocketHandler(tornado.websocket.WebSocketHandler):
    """
    This handles the real-time web socket connection. It pushes the
    new readings everytime the sensor fires. 

    """

    def __init__(self, application, request, **kwargs):
        super(SocketHandler, self).__init__(application, request, **kwargs)
        self.start_odo_thread()
        

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in clients:
            clients.append(self)

    def on_close(self):
        if self in clients:
            clients.remove(self)

    def on_message(self, msg):
        print "got message: ", msg  


    def start_odo_thread(self):
        self.odo = OdometerThread(self).start()



def make_app():


    return tornado.web.Application([
        (r'/', MainHandler),
        (r'/ws', SocketHandler),
        (r'/app/(.*)', tornado.web.StaticFileHandler, {'path':os.path.join(PATH, 'app')})
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()










def sensor(socket):

    # io.setmode(io.BCM)
     
    # pir_pin = 18
    # door_pin = 23
     
    # io.setup(pir_pin, io.IN)         # activate input
    # io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)  # activate input with PullUp

    wheel_circumference = 0.5 * 2 * pi   # wheel diameter in meters
    count = 0
    then = time.time()
    flag = False
    spd = 0.0
    dt = 0.0
    total_dist = 0.0
    while True:
        if io.input(door_pin):
            if flag:
                flag = False
        else:
            if not flag:
                flag = True
                count = count + 1
                now = time.time()
                dt = now - then
                total_dist = total_dist + wheel_circumference
                spd = wheel_circumference / dt   
                text = "count: %s speed: %.1fm/s  dist: %.1fm \r" %(count, spd, total_dist)
		print text
		socket.write_message({'text':text})
		then = now

window.onload = function() {
        DOMAIN = "192.168.0.102:8888";
        SOCKET_URL = "ws://" + DOMAIN + "/ws";
        
        console.log("opening socket connection to " + SOCKET_URL);
        var bgAudio = document.getElementById("bg-audio");
        bgAudio.play();

        updateDisplay = function(data){
            var msgEl = document.getElementById("msg");
            var spdEl = document.getElementById("spd");
            var durationEl = document.getElementById("duration");
            var distEl = document.getElementById("dist");

            //msgEl.innerHTML = data.text;
            spdEl.innerHTML = data.spd.toFixed(1);
            durationEl.innerHTML = data.duration.toFixed(2);
            distEl.innerHTML = data.dist.toFixed(2);


        };

        socket = new WebSocket(SOCKET_URL);

        
        socket.onopen = function(){
            console.log("connection opened....");
            handshake = {"text": "Hello from the browser"};
            var out = JSON.stringify(handshake);
            socket.send(out);
        };

        socket.onmessage = function(msg) {
            /*
            Listens for
            - sensor_values
            - new - This should have a camera IP address un the keyword 'camera_url'. 
            */

            var data = JSON.parse(msg.data);
            console.log("['onmessage'] ", data);
            updateDisplay(data);

        }

        socket.onclose = function(){
            //alert("connection closed....");
            console.log("The connection has been closed.");
            
         }

        socket.onerror = function(){
            console.log("The was an error.");

            console.warn('starting testing data');
            var start, now;
            count = 0;
            start = new Date();
            window.setInterval(function(){
                now = new Date();
                data = {
                    'spd': (Math.random()*10).toFixed(1),
                    'dist': (count * .001).toFixed(2),
                    'duration': ((now - start) / 60).toFixed(2)
                };
                count++;

                updateDisplay(data);
            }, 1000);
         }


    };
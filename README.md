# AutobahnTwistedWebsocket
A simple Python websocket

#A websocket javascript client
```js
        var user = 'Juan';
        //User is needed to authenticate my local user
        var _socket = new WebSocket('ws://127.0.0.1:9000?user=' + user);

        _socket.addEventListener('open', function () {
            console.log('open')
            _socket.send(JSON.stringify({'to': 'Mario', 'from': 'Juan', 'message': 'Hola Mario'}));
        });

        _socket.addEventListener('message', function (e) {
            console.log(e)
        });
```

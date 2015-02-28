# AutobahnTwistedWebsocket
A simple Python websocket

Run the requirements.txt 
`pip install -r > requirements.txt`

Run the server
`python server.py`

###A simple websocket javascript client
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


###A websocket python client

```python
    # Example
    
    def message(message):
        print message
    
    def connect(response):
        print "I am connected callback"
    
    
    socket = SocketMiddleWare()
    socket.set_on_connect(connect)
    socket.set_on_messaget(message)
    socket.connect_socket('Juan')



```
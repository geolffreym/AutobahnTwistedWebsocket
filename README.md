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
    def message(*args, **kwargs):
        print message
    
    
    def connect(*args, **kwargs):
        print "I am connected callback"
    
    
    socket = SocketMiddleWare()
    
    # Event Handlers
    socket.set_on_connect(callback=connect)
    socket.set_on_message(callback=message)
    
    # Run client
    socket.async_connect('Juan')


```
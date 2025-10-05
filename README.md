# Welcom on MultiRaven !

MultiRaven is a simple python server socket that can handle client! He is build on sending Packet and triggering events !

## How To use it:
## Server Side:
### Starting the server:
```python
from multi import Server, server_event_registery

server = Server(host="", port=4444)
server.start_server()
```
This gonna start ther server

### Sending message to all clients:
```python
server.send_to_all("hello_server", "Hello from the server")
```
This will gonna send the packet with the name "hello" to all clients.

### Receving event from a client:
```python
@server_event_registery.on_event("hello_client")
def hello_client(clt, msg, *args):
  print(f"the client:{clt.getpeername()} have seent a msg: {msg}")
```

### To stop the server:
```python
server.stop_server()
```
This will be trigger each tiME the client send a message with packet name: "hello_client"

## Client Side:
### Connect with a client:
```python
from multi import Client, client_event_registery
client = client(ip="127.0.0.1", port=4444)
client.connect() # connecting to the server
```

### To send a msg/data:
```python
client.send("hello_client", "Hello from the client")
```

### Receving event from the server:
```python
@client_event_registery.on_event("hello_server")
def hello_server(clt, msg, *args):
  print(f"You rcved a msg: {msg}")
```

### Disconnecting the clien:
```python
client.disconnect()
```





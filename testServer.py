
import multi
from multi import server_event_registry

@server_event_registry.on_event("hello")
def hello(contents: dict):
    print("hello from the client")
    print(contents)

server = multi.Server()

server.start_server()

input(">>> ")

server.send_to_all("hello", {"msg": "Salut ca va ?"})

input(">>> ")

server.stop_server()

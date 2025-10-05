
import multi
from multi import server_event_registry

@server_event_registry.on_event("hello")
def hello(clt, msg, *args):
    print(f"Hello from the client: {msg=}")

server = multi.Server()

server.start_server()

input(">>> ")

server.send_to_all("hello", "Hello from the server")

input(">>> ")

server.stop_server()

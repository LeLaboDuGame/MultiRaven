
import multi
from multi import client_event_registry

@client_event_registry.on_event("hello")
def hello(contents: dict):
    print("hello from the server")
    print(*contents.values())

client1 = multi.Client()
client2 = multi.Client()


client1.connect()
client2.connect()
input(">>> ")

client1.send("hello", {"msg": "Salut !"})
client2.send("hello", {"msg": "Salut !"})
input(">>> ")

client1.disconnect()
client2.disconnect()

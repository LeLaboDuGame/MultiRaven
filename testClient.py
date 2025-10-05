
import multi
from multi import client_event_registry

@client_event_registry.on_event("hello")
def hello(clt, msg, *args):
    print(f"Message recu de {clt.getpeername()}: {msg}")

client1 = multi.Client()
#client2 = multi.Client()


client1.connect()
#client2.connect()

client1.send("hello","Salut !")
#client2.send("hello","Salut !")

client1.disconnect()
#client2.disconnect()

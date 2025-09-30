import time
import unittest

import multi
from multi import client_event_registry

@client_event_registry.on_event("hello")
def hello(contents: dict):
    print("hello")
    print(*contents.values())


class TestMulti(unittest.TestCase):
    def setUp(self):
        self.server = multi.Server()
        self.client1 = multi.Client()
        self.client2 = multi.Client()

    def test_1_start_server(self):
        print(1)
        self.server.start_server()

    def test_2_clients_connecting(self):
        print(2)
        self.client1.connect()
        self.client2.connect()

    def test_3_send_to_all_clients(self):
        print(3)
        self.server.send_to_all("hello", {"msg": "Salut ca va ?"})
        time.sleep(1)

    def test_4_clients_disconnecting(self):
        print(4)
        self.client1.disconnect()
        self.client2.disconnect()

    def test_5_stop_server(self):
        print(5)
        self.server.stop_server()

import time

from reverb import *

ReverbManager.REVERB_SIDE = [ReverbSide.SERVER, ReverbSide.CLIENT][int(input("1-SERVER\n2-CLIENT\n>>> ")) - 1]


class Player(ReverbObject):
    def __init__(self, pos=[0, 0], dir="N", *reverb_args):
        super().__init__(pos, dir, *reverb_args)
        threading.Thread(target=self.walk)

    def walk(self):
        while True:
            self.dir = input("dir>>> ")
            self.compute_server(self.check_walk, self.dir)

    # ON SERVER
    def check_walk(self, dir):
        print(f"The direction is {dir=}")
        self.dir = dir


if ReverbManager.REVERB_SIDE == ReverbSide.CLIENT:
    clt = Client()
    ReverbManager.REVERB_CONNECTION = clt
    clt.connect()
    while True:
        pass
else:
    serv = Server()
    ReverbManager.REVERB_CONNECTION = serv
    serv.start_server()
    player = Player()
    while True:
        time.sleep(1 / 10)
        ReverbManager.server_sync()

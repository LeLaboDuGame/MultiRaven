import json
import socket
import uuid
from json import JSONDecodeError
from reverb_base import *
from reverb_errors import *
from enum import Enum


class ReverbSide(Enum):
    SERVER=1
    CLIENT=2

class ReverbObject:
    def __init__(self, pos=(0, 0), dir="N", *reverb_args):
        self.dir = dir
        self.pos = pos
        self.reverb_args = reverb_args
        self.uid:str = None
        self.type = self.__class__.__name__
        ReverbManager.add_type_if_dont_exit(self)

    def pack(self):
        """
        :return: A list of all needed args that are linked between the server and the clients
        """
        for arg in self.reverb_args:
            try:
                json.dumps(arg)
            except (TypeError, OverflowError):
                raise Exception(
                    f"The arg: {arg} is not serializable ! It has to be serializable by JSON to be agree as a reverb_args.")
        return {self.type, self.pos, self.dir, *self.reverb_args}

    @staticmethod
    def repack(*datas:classmethod):
        return dict(map(lambda key: (key.__class__.__name__, key), datas))

    def sync(self, pos, dir, *reverb_args):
        if ReverbManager.REVERB_SIDE == "CLIENT":
            self.pos = pos
            self.dir = dir
            if reverb_args != ():
                self.reverb_args = reverb_args
                self.sync_reverb_args()
        else:
            raise ReverbWrongSideError(ReverbManager.REVERB_SIDE)


    def sync_reverb_args(self):
        """
        - Override this function to update your reverb_args.
        - This is only call if you have reverb_args.
        """
        pass

    def is_uid_init(self):
        """
        :return: if uid is init or not
        """
        return self.uid is None

    def get(self):
        pass

class ReverbManager:
    """
    - This class is static !
    - It links ReverbObject to the reference of the ReverbObject !
    """
    REVERB_SIDE:ReverbSide = ReverbSide.SERVER
    REVERB_OBJECTS = {}
    REVERB_OBJECT_REGISTRY = {"ReverbObject": ReverbObject} # Register all type

    @staticmethod
    def print_manager(msg):
        """
        - Print a message with the ReverbManager style
        :param msg: The message
        """
        print(f"{Back.YELLOW + Fore.RED}[{Fore.RESET}REVERB_MANAGER{Fore.RED}]{Style.RESET_ALL} {msg}")

    @staticmethod
    def add_type_if_dont_exit(ro:ReverbObject):
        try:
            ReverbManager.REVERB_OBJECT_REGISTRY[ro.__class__.__name__]
        except KeyError:
            ReverbManager.REVERB_OBJECT_REGISTRY[ro.__class__.__name__] = ro.__class__
            ReverbManager.print_manager(f"Adding type: {ro.__name__} to the registry.")

    @staticmethod
    def get_reverb_object(uid:str) -> ReverbObject:
        """
        - Get the reverb object by uid
        :param uid: The uid
        :return: ReverbObject or ReverbObjectNotFoundError if not found
        """
        try:
            return ReverbManager.REVERB_OBJECTS[uid]
        except KeyError:
            raise ReverbObjectNotFoundError(uid)

    @staticmethod
    def get_cls_by_type_name(t):
        try:
            return ReverbManager.REVERB_OBJECT_REGISTRY[t]
        except KeyError:
            raise ReverbTypeNotFoundError(t)

    @staticmethod
    def add_new_reverb_object(ro:ReverbObject, uid:str="Unknown"):
        """
        - Add a new ReverbObject to the ReverbManager
        :param ro: The ReverbObject
        :param uid: The uid, can be let by default if you are on SERVER side
        """
        if ro in ReverbManager.REVERB_OBJECTS.values(): # Check if the
            if not ro.is_uid_init(): # Check if the RO is not init yet
                if ReverbManager.REVERB_SIDE == ReverbSide.SERVER: # check RM side
                    # SERVER
                        uid = str(uuid.uuid4())
                        ReverbManager.REVERB_OBJECTS[uid] = ro
                else:
                    # CLIENT
                    if uid is not None:
                        ReverbManager.REVERB_OBJECTS[uid] = ro
                    else:
                        raise ReverbUIDNoneError(uid)
            else:
                raise ReverbUIDAlreadyInitError()
        else:
            raise ReverbObjectAlreadyExistError(uid)

        ReverbManager.print_manager(f"New ReverbObject add into '{ReverbManager.REVERB_SIDE}' side with uid={uid}")

    @staticmethod
    @client_event_registry("server_sync")
    def on_server_sync(clt:socket.socket, ros:dict[str, dict[str, object]], *args):
        for uid, ro_data in ros.items():
            try: # try to get a reverb_object
                ro = ReverbManager.get_reverb_object(uid)
                ro_data.pop("type")
                ro.sync(*ro_data)
            except ReverbObjectNotFoundError: # create a new one
                cls = ro_data["type"]
                cls = ReverbManager.get_cls_by_type_name(cls)
                ro_data.pop("type")
                ro = cls(*ro_data.values())
                ReverbManager.add_new_reverb_object(ro)
                ro.sync(*ro_data)

    @staticmethod
    @server_event_registry("")
    def















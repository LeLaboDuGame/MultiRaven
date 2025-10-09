class ReverbWrongSideError(Exception):
    def __init__(self, side):
        super().__init__(f"Wrong side: '{side}' side.")

class ReverbUIDAlreadyInitError(Exception):
    def __init__(self):
        super().__init__("The ReverbObject is already init with uid! Only new ReverbObject can have a new uid!")

class ReverbUIDNoneError(Exception):
    def __init__(self, uid):
        super().__init__(f"The uid {uid} is not valid!")

class ReverbObjectAlreadyExistError(Exception):
    def __init__(self, uid):
        super().__init__(f"The ReverbObject {uid} is already into the ReverbManager!")

class ReverbObjectNotFoundError(Exception):
    def __init__(self, uid):
        super().__init__(f"ReverbObject not found with {uid=}")

class ReverbTypeNotFoundError(Exception):
    def __init__(self, t):
        super().__init__(f"The type={t} is not found into the registry!")
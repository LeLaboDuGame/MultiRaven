# 🎵 Reverb – Multiplayer Game Networking Framework in Python

**Reverb** is an object-oriented networking framework designed to make it easy to create **multiplayer games or applications in Python**.  
It provides an abstraction layer over TCP sockets and automatically handles:

✅ Client/Server connections  
✅ Object synchronization (shared state)  
✅ Server-side function calls from clients  
✅ A simple and extensible event system  
✅ A global object registry (`ReverbObject`)

---

## ✨ Key Features

- 🔌 **Client/Server architecture** using TCP sockets  
- 📦 Simple protocol using **JSON + binary length header**  
- 🧠 Event system (`server_event_registry` / `client_event_registry`)  
- 🔄 Base class **ReverbObject** for synchronized objects  
- 🆔 Automatic **UID management** for objects  
- 🔁 Server → client synchronization (`server_sync()`)  
- 📡 Remote function calls to the server (`compute_server(...)`)  
- 🧭 Detect object ownership (`is_owner()`)  
- 🧱 Clear and extensible API  

---

## 📦 Installation

Currently, Reverb is included directly in the project.  
Include the following files in your project:



> A pip package may be released in the future.

---

## 🚀 Minimal Usage Example

### 1) Select Client or Server

```python
from reverb import ReverbManager, ReverbSide, Client, Server

# Choose side (for example via input)
ReverbManager.REVERB_SIDE = ReverbSide.SERVER  # or ReverbSide.CLIENT
````

---

### 2) Create a ReverbObject

```python
from reverb import ReverbManager, ReverbObject

@ReverbManager.reverb_object_attribute
class Player(ReverbObject):
    def __init__(self, x=0, y=0, uid=None, add_on_init=True, belonging_membership=None):
        self.x = x
        self.y = y
        super().__init__(x, y, uid=uid, add_on_init=add_on_init, belonging_membership=belonging_membership)

    # Optional: called on client when object is created locally
    def on_init_from_client(self):
        pass

    # Optional: called on server when object is created
    def on_init_from_server(self):
        pass
```

---

### 3) Start the Server

```python
if ReverbManager.REVERB_SIDE == ReverbSide.SERVER:
    serv = Server(port=8080)
    ReverbManager.REVERB_CONNECTION = serv
    serv.start_server()

    # Create objects on the server
    player = Player(x=10, y=20)

    # Main loop
    while True:
        # Synchronize objects to clients
        ReverbManager.server_sync()
```

---

### 4) Start a Client

```python
if ReverbManager.REVERB_SIDE == ReverbSide.CLIENT:
    clt = Client(ip="127.0.0.1", port=8080)
    ReverbManager.REVERB_CONNECTION = clt
    clt.connect()

    # Main loop
    while True:
        # Access synchronized objects
        for p in ReverbManager.get_all_ro_by_type(Player):
            print(p.x, p.y)
```

---

## 🧠 How It Works

### 🔹 1. `ReverbObject`

The base class for all synchronized objects.
It contains:

* Object variables (defined in `__init__`)
* A unique `uid`
* `belonging_membership` = client port owning the object
* Optional callbacks:

  * `on_init_from_server()`
  * `on_init_from_client()`

### 🔹 2. `ReverbManager`

* Tracks all ReverbObjects (`REVERB_OBJECTS`)
* Stores side (SERVER or CLIENT)
* Synchronizes objects (`server_sync()`)
* Automatically creates objects on the client
* Allows clients to call server functions (`compute_server()`)

### 🔹 3. Network Events

* `server_event_registry` → server-side events (e.g., client connection)
* `client_event_registry` → client-side events (e.g., object sync, disconnect)
* Easily extendable using decorators `@...on_event("...")`

---

## 🔁 Automatic Synchronization

Server-side:

```python
ReverbManager.server_sync()
```

→ Sends the state of all objects to all clients

Client-side:

The `"server_sync"` event automatically updates or creates objects locally.

---

## 📡 Server Function Call (RPC)

```python
# Client-side
obj.compute_server(obj.my_func, arg1, arg2)
```

→ Executes `obj.my_func(arg1, arg2)` on the server.

---

## ✅ Check Object Ownership

```python
if obj.is_owner():
    # This client controls the object
```

---

## ⚠️ Current Limitations

❌ No advanced network error handling
❌ No compression or delta-sync (full state sent each sync)
❌ No authentication or data security
❌ No latency handling or interpolation
❌ Single listener thread per client (no advanced optimizations)

---

## 📝 TODO / Possible Improvements

* [ ] Create a pip package
* [ ] Add client-side interpolation
* [ ] Optimize synchronizations (deltas, priorities, frequency)
* [ ] Authentication / network security
* [ ] Logging and monitoring
* [ ] Debugging tools (object viewer)
* [ ] Room / channel management
* [ ] Protocol versioning / compatibility

---

## 🙌 Contribution

This project is in active development.
Feedback, suggestions, and contributions are welcome!

```

Do you want me to do that?
```

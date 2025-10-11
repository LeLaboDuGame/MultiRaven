
# PyReverb

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

A lightweight Python networking framework for real-time client-server synchronization of objects, designed for multiplayer game development and interactive simulations.

---

## Table of Contents
- [What the Project Does](#what-the-project-does)
- [Why the Project is Useful](#why-the-project-is-useful)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage Example](#usage-example)
- [Support](#support)
- [Contributing](#contributing)

---

## What the Project Does

Reverb is a Python framework that allows you to create synchronized networked objects across a client-server architecture. It provides:

- Event-driven networking with automatic packet handling.
- Simple creation and synchronization of "ReverbObjects" across clients and servers.
- Client-server communication for executing functions remotely.
- Built-in registry for managing objects and types efficiently.

It is ideal for building multiplayer games, simulations, or collaborative applications where objects need to stay in sync in real-time.

---

## Why the Project is Useful

Key benefits:

- **Real-time synchronization:** Keep objects consistent across multiple clients automatically.
- **Event-driven architecture:** Easily react to client connections, disconnections, and custom events.
- **Lightweight and extensible:** Minimal dependencies (`colorama`, `pygame`) and easy to extend for custom object types.
- **Cross-side operations:** Compute on server from client, with ownership checks and safe data management.
- **Simple networking abstractions:** Handles raw socket communication, packet encoding/decoding, and threading.

---

## Getting Started

### Installation

1. Clone the repository:

```bash
git clone https://github.com/LeLaboDuGame/PyReverb.git
cd reverb
````

2. Install dependencies:

```bash
pip install -r requirements.txt
```

> `requirements.txt` should include:
>
> ```text
> colorama
> pygame
> ```

3. Run examples:

```bash
python Exemple.py
```

---

### Usage Example

```python
from reverb import ReverbManager, ReverbSide, ReverbObject, Client, Server, ReverbManager

# Set the side (SERVER or CLIENT)
ReverbManager.REVERB_SIDE = ReverbSide.SERVER

# Define a networked object
@ReverbManager.reverb_object_attribute
class Player(ReverbObject):
    def __init__(self, pos=[0, 0], uid=None, add_on_init=True):
        self.pos = pos
        super().__init__(pos, uid=uid, add_on_init=add_on_init)

    def on_init_from_client(self):
        print("Player initialized on client")

    def on_init_from_server(self):
        print("Player initialized on server")

# Start server
server = Server()
ReverbManager.REVERB_CONNECTION = server
server.start_server()
```

On the client side:

```python
ReverbManager.REVERB_SIDE = ReverbSide.CLIENT
client = Client()
ReverbManager.REVERB_CONNECTION = client
client.connect()
```

The `ReverbManager` handles automatic synchronization of `ReverbObject` instances between server and clients.

---

## Support

* For issues and bug reports, use the [GitHub Issues](issues) page.
* Documentation and API references are available in the `docs/` folder.
* Community discussions can be held in the repository discussions section.

---

## Contributing

Contributions are welcome! Please follow the [CONTRIBUTING.md](docs/CONTRIBUTING.md) guidelines.

Typical contributions include:

* Adding new features or `ReverbObject` types.
* Improving networking performance.
* Fixing bugs and improving documentation.

---

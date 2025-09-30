import json
import socket
import threading
from json import JSONDecodeError
from warnings import warn

from colorama import Fore, Back, Style


class EventRegistry:
    def __init__(self):
        """
        A Class that store events and handle them !
        """
        self._events = {}

    def on_event(self, event_name):
        """
        Simple decorator to trigger events
        :param event_name: The name of the event
        :return: The decorator
        """

        def decorator(func):
            if event_name not in self._events:
                self._events[event_name] = []
            self._events[event_name].append(func)
            return func

        return decorator

    def get(self, event_name):
        """
        Get an event by his name
        :param event_name: The name of the event
        :return: Event functions
        """
        return self._events.get(event_name)

    def trigger(self, event_name, *args, **kwargs):
        """
        Trigger an event
        :param event_name: The name of the event
        """
        handlers = self._events.get(event_name, [])  # Check if the event name contain functions or not
        if handlers:
            for handler in handlers:
                try:
                    handler(*args, **kwargs)
                except TypeError:
                    handler()
        else:
            warn(f"The handler for '{event_name}' is not found ! It may be normal, ignore then.")

    def all_events(self):
        """
        :return: All events
        """
        return list(self._events.keys())


client_event_registry = EventRegistry()
server_event_registry = EventRegistry()


class Packet:
    @staticmethod
    def create_packet(name: str, content: dict):
        """
        Create a packet and encode it
        :param name: Name of the packet/event
        :param content: The contents to send
        :return: An encoded packet ready to be sent :)
        """
        return json.dumps({"name": name, "contents": content}).encode()

    @staticmethod
    def decode_packet(packet: bytes):
        """
        Decode the packet from a bytes
        :param packet: The encoded packet
        :return: The name/event and the contents
        """
        try:
            decoded_packet = json.loads(packet.decode())
            return decoded_packet["name"], decoded_packet["contents"]
        except JSONDecodeError:
            print(f"An error occurred with this packet: {packet.decode()}")
        except KeyError:
            print(f"The packet is not valid ! A valid packet must have a 'name' and a 'contents' argument !")


class Client:
    def __init__(self, ip="127.0.0.1", port=4444, buffer_size=1024):
        self.buffer_size = buffer_size
        self.port = port
        self.ip = ip
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False

    def connect(self):
        """
        Call to connect to the server
        """
        try:
            self.client.connect((self.ip, self.port))
            self.is_connected = True

            threading.Thread(target=self.listen, daemon=True)
            client_event_registry.trigger("connection")

        except ConnectionRefusedError:
            Client.print_client("The server is unreachable !")
        except socket.gaierror:
            Client.print_client("Error with host name or IP unfound")
        except TimeoutError:
            Client.print_client("Connexion TimeOut !")

    def listen(self):
        """
        Thread that listen for new content from the server
        """

        while self.is_connected:
            try:
                packet = self.client.recv(self.buffer_size)

                if packet:
                    packet_name, contents = Packet.decode_packet(packet)
                    client_event_registry.trigger(packet_name, contents)
                else:
                    warn("The server send an empty packet !")
            except ConnectionResetError:
                Client.print_client("Connexion lost !")
                self.client.close()

    def send(self, packet_name: str, content: dict):
        """
        Send a content to the server
        :param packet_name: The name of the packet
        :param content: contents
        """
        if self.is_connected:
            packet = Packet.create_packet(packet_name, content)
            self.client.send(packet)

    def disconnect(self):
        """
        Call to disconnect the user
        """
        self.send("client_disconnection", {"addr": self.client.getpeername()})
        self.client.close()
        self.is_connected = False
        client_event_registry.trigger("disconnection")

    @staticmethod
    def print_client(msg):
        """
        Print a message with client style
        :param msg: the message to print
        """
        print(f"{Back.BLUE + Fore.RED}[{Fore.RESET}CLIENT{Fore.RED}]{Style.RESET_ALL} {msg}")


class Server:
    def __init__(self, host="", port=4444, buffer_size=1024):
        self.buffer_size = buffer_size
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_online = False
        self.clients = {}

    @staticmethod
    def print_server(msg):
        """
        Print a message with server style
        :param msg: the message to print
        """
        print(f"{Back.GREEN + Fore.RED}[{Fore.RESET}SERVER{Fore.RED}]{Style.RESET_ALL} {msg}")

    def start_server(self):
        """
        Start the server
        """
        Server.print_server("Starting server...")
        self.server.bind(("", self.port))
        self.server.listen()

        Server.print_server(f"Server online ! Waiting for clients on {self.host}:{self.port}...")
        self.is_online = True
        threading.Thread(target=self._accept_clients, daemon=True).start()

    def stop_server(self):
        """
        Stop the server
        """
        self.is_online = False
        for client in self.clients:
            client.send(Packet.create_packet("server_stop"))
            Server.print_server(f"The client: {client.getpeername()} is disconnect !")
            client.close()
        Server.print_server("All player disconnected.")

        if self.server:
            self.server.close()
        Server.print_server("Server closed !")

    def _accept_clients(self):
        """Thread that accept clients when they connect to the server"""
        while self.is_online:
            client_socket, addr = self.server.accept()
            self.clients[addr] = client_socket
            Server.print_server(f"Client connected on: {addr}")
            threading.Thread(target=self._handle_client, args=(client_socket, addr), daemon=True).start()

    def _handle_client(self, client_socket, addr):
        """Thread that trigger event from packet recv from clients"""
        try:
            while self.is_online:
                try:
                    packet = client_socket.recv(self.buffer_size)
                    print(f"Packet rcv: {packet.decode()}")
                    packet_name, contents = Packet.decode_packet(packet)
                    print(packet_name, " | ", contents)
                    server_event_registry.trigger(packet_name, contents.values)
                except ConnectionResetError:
                    Server.print_server(f"The client at add: {addr} has been disconnected ! This is an anomaly.")
        finally:
            if addr in self.clients:
                self.clients.pop(addr)
            client_socket.close()
            Server.print_server(f"The client: {addr} is disconnect !")

    def send_to_all(self, packet_name, contents):
        """
        Send a packet to all player
        :param packet_name: The name of the packet/event
        :param contents: Contents
        """
        self.server.sendall(Packet.create_packet(packet_name, contents))


# Basic Event Registry

# SERVER EVENTS
@server_event_registry.on_event("client_disconnection")
def on_client_disconnect(addr, *args):
    Server.print_server(f"The client: {type(addr)} {args} disconnect itself ! (Client Side)")


# CLIENT EVENTS
@client_event_registry.on_event("connection")
def on_connection():
    Client.print_client("Client is connecting !")


@client_event_registry.on_event("disconnection")
def on_disconnection():
    Client.print_client("Client disconnecting.")

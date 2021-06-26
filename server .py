from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

# Defining socket variables
s = socket(AF_INET, SOCK_STREAM)
print("socket created")
port = 9999
s.bind(('', port))


# initialising dictionary
dict_address = {}
online = {}


def accept_client_connections():
    while True:
        client, client_address = s.accept()
        dict_address[client] = client_address
        print("%s:%s has connected" % client_address)
        Thread(target=client_handler, args=(client,)).start()


def client_handler(client):
    name = client.recv(1024).decode("utf8")
    online[client] = name

    welcome_message = "Welcome"+" "+name+" "+"!!"
    client.send(bytes(welcome_message, "utf8"))
    time.sleep(1)
    online_list_updater()

    while True:
        incoming_message = client.recv(1024)
        if incoming_message != bytes("/exit", "utf8"):
            if incoming_message == bytes("online", "utf8"):
                client.send(bytes(str(online.values()), "utf8"))

            elif incoming_message == bytes("/private", "utf8"):
                client.send(
                    bytes("Let us know who you want to message", "utf8"))
                private = client.recv(1024).decode()
                client.send(bytes("enter message", "utf8"))
                private_message = client.recv(1024).decode()
                private_socket = obtain_key_from_value(private)
                private_socket.send(
                    bytes('[Private]' + name+': ' + private_message, "utf8"))
                client.send(bytes('[Private]' + name +
                                  ': ' + private_message, "utf8"))

            else:
                outgoing_message_handler(incoming_message, name+": ")

        elif incoming_message == bytes("/exit", "utf8"):
            client.close()
            del online[client]
            del dict_address[client]
            online_list_updater()
            outgoing_message_handler(
                bytes("%s has left the chat" % name, "utf8"))
            break


def outgoing_message_handler(message, prefix=': '):

    for i in dict_address:
        try:
            i.send(bytes(prefix, "utf8")+message)
        except OSError:
            print("OSError Caught")
    print(message.decode("utf8"))


def online_list_updater():
    online_list = "update"+" " + str(online.values())
    for sock in dict_address:
        sock.send(bytes(online_list, "utf8"))


def obtain_key_from_value(val):
    for key, value in online.items():
        if val == value:
            return key


if __name__ == "__main__":

    s.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_client_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    s.close()
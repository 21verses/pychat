from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread
from tkinter import *
import time
import tkinter.font as TkFont
from PIL import ImageTk, Image
from sys import exit

online_list = set()
printed = []


def message_handler_outgoing(event=None):
    message = client_message.get()
    client_message.set("")
    sock.send(bytes(message, "utf8"))
    if message == "/exit":
        sock.close()
        top.destroy()
        exit(0)






def message_handler_incoming():
    while True:
        try:
            msg = sock.recv(1024).decode("utf8")
            if msg.startswith("update"):
                dict_online_str = msg.replace("update", "")
                dict_online_str = dict_online_str.replace("dict_values([", "")
                dict_online_str = dict_online_str.replace("])", "")
                list_online = dict_online_str.split(',')
                Lb1.delete(0, END)
                Lb1.insert(0, "People Online Right Now")

                for i in list_online:
                    Lb1.insert(1, i)
                    Lb1.pack()

            else:
                message_container.insert(END, msg)
                message_container.yview(END)

        except OSError:
            break


top = Tk()

top.title("Discover")


messages_frame = Frame(top, bd=5, width=90, height=40)


client_message = StringVar()
client_message.set("")

scrollbar = Scrollbar(messages_frame)
scrollbar.pack(side=RIGHT, fill=Y)

messages_font = TkFont.Font(family="Times", size=15, weight="normal")
message_container = Listbox(messages_frame, bg="#e6bef7", font=messages_font,
                            fg="#3d0091", width=70, height=20, yscrollcommand=scrollbar)

message_container.pack(side=LEFT, fill=BOTH, expand=True)
message_container.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=message_container.yview)
messages_frame.pack()


type_here = Entry(top, textvariable=client_message, width=50)
type_here.bind("<Return>", message_handler_outgoing)
type_here.pack()
Lb1 = Listbox(messages_frame, bd=5, width=25, bg="#f2858b",
              font=messages_font, fg="#087054")


sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('127.0.0.1', 9999))
thread1 = Thread(target=message_handler_incoming)
thread1.start()
mainloop()

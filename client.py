import socket
from tkinter import *
from threading import Thread
import random
from tkinter import ttk

PORT = 5500
IP_ADDRESS='127.0.0.1'
SERVER= None
BUFFER_SIZE=4096

name=None
listbox=None
textarea=None
text_message=None

def connectionToServer():
    global  SERVER,name

    clientname=name.get()
    SERVER.send(clientname.encode("utf-8"))

def showClientList():
    global SERVER

    SERVER.send("show_list".encode("utf-8"))

def connectWithClient():
    global SERVER

    SERVER.send("connect".encode("utf-8"))

def disconnectWithClient():
    global SERVER

    SERVER.send("disconnect".encode("utf-8"))

def sendButton():
    global SERVER

    SERVER.send("send".encode("utf-8"))

def recieveMessage():
    global SERVER

    while True:
        try:
            message=SERVER.recv(BUFFER_SIZE)
            print("what msg the client received",message)
        except:
            pass
    
def openChatWindow():

    window=Tk()

    window.title('Messenger')
    window.geometry("500x400")
    
    global name,listbox,textarea,text_message

    namelabel= Label(window, text= "Enter Name Here",font = ("Arial",10))
    namelabel.place(relx=0.05,rely=0.07)

    name=Entry(window,width=30,font=("Arial",10))
    name.place(relx=0.28,rely=0.07)

    connectserver= Button(window,text="Connect to Chat Server",bd=1,font=("Arial",10),command=connectionToServer)
    connectserver.place(relx=0.70,rely=0.07)

    separator=ttk.Separator(window,orient='horizontal')
    separator.place (relx=0,rely=0.15,relwidth=1,relheight=0.01)

    labelusers= Label(window, text="Active Users",font=("Arial",10))
    labelusers.place(relx=0.1,rely=0.20)

    listbox= Listbox(window,height=5,width=60,font=("Arial",10))
    listbox.place(relx=0.1,rely=0.25)

    scrollbar1 = Scrollbar(listbox)
    scrollbar1.place(relheight=1,relx=0.97)
    scrollbar1.config(command=listbox.yview)

    connectButton=Button(window,text="Connect",bd=1,font=("Arial",10),command=connectWithClient)
    connectButton.place(relx=0.60,rely=0.5)

    disconnectButton=Button(window,text="Disconnect",bd=1,font=("Arial",10),command=disconnectWithClient)
    disconnectButton.place(relx=0.72,rely=0.5)

    refreshButton=Button(window,text="Refresh",bd=1,font=("Arial",10),command=showClientList)
    refreshButton.place(relx=0.87,rely=0.5)

    labeltext= Label(window, text="Chat Window",font=("Arial",10))
    labeltext.place(relx=0.1,rely=0.58)

    textarea=Text(window,width=60,height = 5,font=("Arial",10))
    textarea.place(relx=0.1,rely=0.62)

    scrollbar2 = Scrollbar(textarea)
    scrollbar2.place(relheight=1,relx=0.97)
    scrollbar2.config(command=textarea.yview)

    attach=Button(window,text="Attach and Send",bd=1,font=("Arial",10))
    attach.place(relx=0.1,rely=0.85)

    text_message= Entry(window,width=30, font=("Arial",10))
    text_message.place(relx=0.32,rely=0.86)

    send=Button(window,text="send",bd=1,font=("Arial",10),command=sendButton)
    send.place(relx=0.85,rely=0.85)

    filepathLabel= Label(window,text="Path of File",font=("Arial",10),bg="green",fg="white")
    filepathLabel.place(relx=0.1,rely=0.92)


    window.mainloop()


def setup():
    global PORT,SERVER,IP_ADDRESS,BUFFER_SIZE,clients

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS,PORT))

    thread=Thread(target=recieveMessage)
    thread.start()

    print("client connected")
    openChatWindow()
    
setup()

import socket
from threading import Thread

ip_address='127.0.0.1'
port=5500
server=None
clients={}
buffer_size=None

def removeClient(client_name):
    pass

def sendTextMessages(client_name,message):
    pass

def handleErrorMessage(client):
    pass

def handleShowList(client):
    pass

def connectedWithClient(message,client,client_name):
    pass

def disconnectedWithClient(message,client,client_name):
    pass

def handleSendFile(client_name,file_name,file_size):
    pass

def grantAccess(client_name):
    pass

def declineAccess(client_name):
    pass

def handleMessages(client,message,client_name):

    if(message == "show_list"):
        print("show_list")
        handleShowList(client)
    elif(message[:7]=="connect"):
        connectedWithClient(message,client,client_name)
    elif(message[:10]=="disconnect"):
        disconnectedWithClient(message,client,client_name)
    elif(message[:4]=="send"):
        file_name=""
        file_size=""
        handleSendFile(client_name,file_name,file_size)
    elif(message == "y" or message=="yes"):
        grantAccess(client_name)
    elif(message == "n" or message=="no"):
        declineAccess(client_name)

    else:
        connected=clients[client_name]["connected_with"]
        if(connected):
            sendTextMessages(client_name,message)
        else:
            handleErrorMessage(client)

def handleClient(client,client_name):
    global ip_address,server,port,clients,buffer_size
    wlM="Welcome idkidkidk"
    client.send(wlM.encode())

    while True:
        try:
            buffer_size=clients[client_name]["file_size"]
            chunk=client.recv(buffer_size)
            message=chunk.decode().strip().lower()
            print("what is msg from client:",message)
            if(message):
                handleMessages(client,message,client_name)
            else:
                removeClient(client_name)
        except:
            pass

def acceptConnections():
    global ip_address,server,port,clients,buffer_size
    while True:
        client,addr=server.accept()
        client_name=client.recv(4098).decode().lower()
        clients[client_name]={
            "client":client,
            "address":addr,
            "connected_with":"",
            "file_name":"",
            "file_size":4096
        }
        print(f"Connected with {client_name}:{addr}")
        print(clients)
        thread=Thread(target=handleClient,args={client,client_name})
        thread.start

def setup():
    global ip_address,server,port,clients

    server= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((ip_address,port))

    server.listen(100)

    print("Server Started")

    acceptConnections()

setup()
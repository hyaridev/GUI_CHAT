import socket
import threading 

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Broadcast Function: Sends A message to all the connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle: handle the individual connenctions to the client

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]} says {message}")
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            break
        

# Receive: The Function which will listen and accept new connections
# This function will be the main function running in the main thread.
#we are gonna run multiple handle functions/ threads
def recieve():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")
        
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024)
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} has joined the chat!\n".encode('utf-8'))
        client.send("Connected to the chat".encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server Running...")
recieve()
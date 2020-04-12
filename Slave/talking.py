import socket
import json

def send(client : socket.socket,data : str):
    client.send(str(len(data)).encode('utf-8'))
    client.recv(2)
    client.send(data.encode('utf-8'))

def recv(client : socket.socket):
    lenght = int(client.recv(100).decode('utf-8'))
    client.send('OK'.encode('utf-8'))
    recv = client.recv(lenght)
    return recv.decode('utf-8')

def request(client : socket.socket, data : str):   
    #return json.dumps({'cmd':'get_links','parm':['https://steemit.com/']})
    send(client,data)   
    return recv(client)
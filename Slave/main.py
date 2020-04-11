import socket
import json

PORT = 4455
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect((socket.gethostname(),PORT))

toSay = json.dumps({
            'cmd':'AnyWork'
            #'cmd':'found_sites',
            #'parm':['www.fdsgf.de','https://fsfgd.org']
        })

#send
client.send(str(len(toSay)).encode('utf-8'))
client.recv(2)
client.send(toSay.encode('utf-8'))

#recv 

lenght = int(client.recv(100).decode('utf-8'))
client.send('OK'.encode('utf-8'))
recv = client.recv(lenght)
print(recv.decode('utf-8'))

client.close()
import socket
import time
import dbmanager
import json
from threading import Thread

PORT = 4455
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


class handle:
    def __init__(self,client : socket.socket):
        self.client = client
        self.running_thread = Thread(target=self.handle)
        self.running_thread.daemon = True
        self.running_thread.start()

    def handle(self):
        data = self.recv_data()
        obj = json.loads(data)
        response = {
            'cmd':'unknown',
            'parm': []
        }

        if obj['cmd'] == 'AnyWork':
            response = self.search_work()

        self.send_data(json.dumps(response))
        self.client.close()

    def search_work(self):
        url = dbmanager.openSites_find_unworked()
        if url == None:
            return {
                'cmd':'nothing',
                'parm':[]  }
        dbmanager.openSites_update_state(str(url),1)

        parm = []
        parm.append(str(url))
        return {
            'cmd':'ok',
            'parm':parm
        }



    def send_data(self,data : str):
        dataLenght = len(data)
        self.client.send(str(dataLenght).encode('utf-8'))

        #Wait for an answer
        self.client.recv(2)

        self.client.send(data.encode('utf-8'))


    def recv_data(self):
        recv = self.client.recv(100).decode('utf-8')
        dataLenght = int(recv)

        self.client.send('OK'.encode('utf-8'))

        buffer = self.client.recv(dataLenght)
        return buffer.decode('utf-8')


def swarm_run():       
    server.bind((socket.gethostname(),PORT))
    server.listen(5)
    print("Listening...")

    while True:
        (client,address) = server.accept()
        h = handle(client)
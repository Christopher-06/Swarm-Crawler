import socket
import time
import dbmanager
import json
from threading import Thread

PORT = 4455
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
swarm_run_thread = None


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

        if obj['cmd'] == 'exit':
            response = {'cmd':'ok','parm':[]}

        if obj['cmd'] == 'AnyWork':
            response = self.search_work()

        if obj['cmd'] == 'found_sites':
            response = self.found_sites(obj['parm'])

        if obj['cmd'] == 'get_links_done':
            response = self.get_links_done(obj['parm'][0])

        self.send_data(json.dumps(response))
        self.client.close()

    def search_work(self):
        #find unsearched sites
        url = dbmanager.openSites_find_unworked()

        if url == None:
             #research a site:
            url = dbmanager.closedSites_get_random()
        if url == None:
           #no site is avaible to search/research          
            return {
                'cmd':'nothing',
                'parm':[]  }

        if dbmanager.openSites_contains(str(url)) == False:
            dbmanager.openSites_insert_new(str(url))            

        dbmanager.closedSites_remove(str(url))
        dbmanager.openSites_update_state(str(url),1)
        return {
            'cmd':'get_links',
            'parm':[str(url)]
        }

    def found_sites(self,sites):
        for site in sites:
            if dbmanager.openSites_contains(site) == False and dbmanager.closedSites_contains(site) == False:
                dbmanager.openSites_insert_new(site)
                print(site)
        return {'cmd':'ok','parm':[]}

    def get_links_done(self,url):
        print("Finished: " + url)
        dbmanager.openSites_remove_item(url)
        dbmanager.closedSites_insert(url)

        return {'cmd':'ok','parm':[]}

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

def swarm_start():
    swarm_run_thread = Thread(target=swarm_run)
    swarm_run_thread.daemon = True  
    swarm_run_thread.start()
    time.sleep(1)

def swarm_run():       
    server.bind((socket.gethostname(),PORT))
    server.listen(5)
    print("Listening...")

    while True:
        (client,address) = server.accept()
        h = handle(client)

def swarm_stop():
    print("Stopping swarm...")    
    server.close()
    print("Stopped swarm succesfully")

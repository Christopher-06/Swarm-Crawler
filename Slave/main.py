import socket
import json, time
from threading import Thread
import talking
import dbmanager
import crawler
from bs4 import BeautifulSoup
import requests
import re
import random

PORT = 4455

getWork = json.dumps({
            'cmd':'AnyWork'
            #'cmd':'found_sites',
            #'parm':['www.fdsgf.de','https://fsfgd.org']
        })

def run():
    while True:
        #prepare new iteration
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((socket.gethostname(),PORT))        
        dbmanager.closedSites_delete_all()
        dbmanager.openSites_delete_all()


        #get job
        job = {}
        while True:
            job = json.loads(talking.request(client,getWork))
            if job['cmd'] == 'get_links':
                break
            print("No work to do!")
            time.sleep(5)
        client.close()

        #do job
        url = job['parm'][0]
        current_domain = crawler.extract_domain(url)
        crawler.get_all_links(url)
        dbmanager.closedSites_insert(url)

        #say the site is finished        
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((socket.gethostname(),PORT))                                 
        talking.request(client,json.dumps({'cmd':'get_links_done','parm':[url]}))
        client.close()

        #read all other pages
        while True:
            url = dbmanager.openSites_get()
            if url == None:
                break
            
            dbmanager.closedSites_insert(url)
            dbmanager.openSites_remove(url)

            if current_domain in crawler.extract_domain(url):
                crawler.get_all_links(url)

            if dbmanager.syncSites_contains(crawler.extract_domain(url)) == False:
                    dbmanager.syncSites_insert(crawler.extract_domain(url))

            if random.randint(0,5) == 3:
                sync_sites()

            time.sleep(1)


        #end     
        print("Next iteration...")   
        time.sleep(5)

def sync_sites():
    print("sync domains")
    domains = dbmanager.syncSites_get_all()
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((socket.gethostname(),PORT))                                 
    talking.request(client,json.dumps({'cmd':'found_sites','parm':domains}))
    client.close()
    

def main():
    dbmanager.init_db()
    run_thread = Thread(target=run)
    run_thread.daemon = True
    run_thread.start()

    while True:
        INPUT = input()

        if INPUT == 'break' or INPUT == 'exit':
            break



if __name__ == "__main__":
    main()
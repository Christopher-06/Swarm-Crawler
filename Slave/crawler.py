from bs4 import BeautifulSoup
import requests
import re
import time
import dbmanager

def extract_domain(url : str):
    return re.sub(r'(.*://)?([^/?]+).*', '\g<1>\g<2>', url)

def get_all_links(url : str):
    domain = extract_domain(url)
    print("-------------------------------")
    print('Get links from: ' + url)
    for i in range(5):
        try:
            page = requests.get(url)    
            data = page.text
            soup = BeautifulSoup(data,'html.parser')            
            for link in soup.find_all('a'):
                a = str(link.get('href'))
                if '#' in a or a == 'None':
                    continue

                site = a
                if 'http' in site and '://' in site or 'www.' in site:
                    site = a
                else:
                    site = domain + a

                site = site.partition('?')[0]

                if dbmanager.openSites_contains(site) == False and dbmanager.closedSites_contains(site) == False:
                    dbmanager.openSites_insert_new(site)   
            break          
        except:
            print("Failed. Trying again...")
            time.sleep(2)
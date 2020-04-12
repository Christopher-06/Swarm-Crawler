import sqlite3
import os.path
from random import randint

DATABASE_NAME = 'db.sqlite'

def init():
    #Init sqlite database
    dbHasToInit = False
    if os.path.isfile(DATABASE_NAME) == False:
        dbHasToInit = True

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    if dbHasToInit == True:
        cursor.execute('CREATE TABLE closedSites(url TEXT)')
        cursor.execute('CREATE TABLE openSites(url TEXT,state INT)')

        cursor.execute("INSERT INTO openSites(url,state) VALUES(?,?)",('https://windthorst-gymnasium.de/',0,))
        conn.commit()

    #setting all openSites to 0 --> Otherwise it will not be searched after restart
    cursor.execute("UPDATE openSites SET state=0")
   # cursor.execute("INSERT INTO closedSites(url) VALUES(?)",('fggdg',))
    conn.commit()
    conn.close()

#region Closed Sites Methods
def closedSites_remove(url : str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM closedSites WHERE url=?",(url,))
    conn.commit()

    cursor.close()
    conn.close()  

def closedSites_insert(url : str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO closedSites(url) VALUES(?)",(url,))
    conn.commit()
    cursor.close()
    conn.close()

def closedSites_contains(url : str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM closedSites WHERE url=?',(url,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()  
    for row in rows:
        return True

    return False

def closedSites_get_random():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM closedSites')
    rows = cursor.fetchall()
    url = None

    cursor.close()
    conn.close()  
    for row in rows:
        if randint(0,5) == 0 or url == None:
            url = row[0]

    return url
#endregion

#region Open Sites Mehtods
def openSites_find_unworked():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM openSites WHERE state=0")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()    

    for row in rows:
        return row[0]

    return None

def openSites_remove_item(url : str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM openSites WHERE url=?",(url,))
    conn.commit()

    cursor.close()
    conn.close()  

def openSites_update_state(url : str,state: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE openSites SET state=? WHERE url=?",(state,url))
    conn.commit()
    cursor.close()
    conn.close()

def openSites_insert_new(url : str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO openSites(url,state) VALUES(?,?)",(url,0,))
    conn.commit()

    cursor.close()
    conn.close()  


def openSites_contains(url : str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM openSites WHERE url=?',(url,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()  

    for row in rows:
        return True

    return False
#endregion
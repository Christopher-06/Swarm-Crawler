import sqlite3
import os.path


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

        cursor.execute("INSERT INTO openSites(url,state) VALUES(?,?)",('https://steemit.com',0,))
        conn.commit()

    #setting all openSites to 0 --> Otherwise it will not be searched after restart
    cursor.execute("UPDATE openSites SET state=0")
    conn.commit()
    conn.close()

#region Closed Sites Methods
def closedSites_insert(url : str):
    cursor.execute("INSERT INTO closedSites(url) VALUES(?)",(url,))
    conn.commit()

def closedSites_contains(url : str):
    cursor.execute('SELECT * FROM closedSites WHERE url=?',(url,))
    rows = cursor.fetchall()

    for row in rows:
        return True

    return False
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
    cursor.execute("DELETE FROM openSites WHERE url=?",(url,))
    conn.commit()

def openSites_update_state(url : str,state: int):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE openSites SET state=? WHERE url=?",(state,url))
    conn.commit()
    cursor.close()
    conn.close()

def openSites_insert_new(url : str):
    cursor.execute("INSERT INTO openSites(url,state) VALUES(?,?)",(url,0,))
    conn.commit()

def openSites_contains(url : str):
    cursor.execute('SELECT * FROM openSites WHERE url=?',(url,))
    rows = cursor.fetchall()

    for row in rows:
        return True

    return False
#endregion
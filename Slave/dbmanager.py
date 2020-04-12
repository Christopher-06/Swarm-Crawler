import os.path,sqlite3

DATABASE_NAME = 'db.sqlite'


def init_db():
    dbHasToInit = False
    if os.path.isfile(DATABASE_NAME) == False:
        dbHasToInit = True
    
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    if dbHasToInit == True:
        cursor.execute('CREATE TABLE closedSites(url TEXT)')
        cursor.execute('CREATE TABLE openSites(url TEXT)') 
        cursor.execute('CREATE TABLE syncSites(url TEXT)')            

    cursor.execute('DELETE FROM closedSites')
    cursor.execute('DELETE FROM syncSites')
    cursor.execute('DELETE FROM openSites')
    conn.commit()

    cursor.close()
    conn.close()

def syncSites_delete_all():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM syncSites')
    conn.commit()
    cursor.close()
    conn.close() 

def syncSites_get_all():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM syncSites')
    rows = cursor.fetchall()

    cursor.close()
    conn.close()  
    l = []
    for row in rows:
            l.append(row[0])

    return l

def syncSites_insert(url : str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO syncSites(url) VALUES(?)",(url,))
    conn.commit()
    cursor.close()
    conn.close()

def syncSites_contains(url : str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM syncSites WHERE url=?',(url,))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()  

    for row in rows:
        return True

    return False





def closedSites_delete_all():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM closedSites')
    conn.commit()
    cursor.close()
    conn.close() 

def closedSites_get():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM closedSites')
    rows = cursor.fetchall()

    cursor.close()
    conn.close()  
    for row in rows:
            return row[0]

    return None

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

def openSites_delete_all():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM openSites')
    conn.commit()
    cursor.close()
    conn.close()

def openSites_remove(url : str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM openSites WHERE url=?",(url,))
    conn.commit()

    cursor.close()
    conn.close() 

def openSites_get():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM openSites")
    rows = cursor.fetchall()

    cursor.close()
    conn.close()    

    for row in rows:
        return row[0]

    return None

def openSites_insert_new(url : str):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO openSites(url) VALUES(?)",(url,))
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
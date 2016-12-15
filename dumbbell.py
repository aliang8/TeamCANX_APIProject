import sqlite3 as sql
import hashlib

#CONNECT DATABASE
DATA = "data/dumbbell.db"

#Initialize databases. Only works once.
def initializeTables():
    db = sql.connect(DATA)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS accounts (username TEXT NOT NULL, password TEXT NOT NULL, userID INTEGER PRIMARY KEY autoincrement)")
    c.execute("CREATE TABLE IF NOT EXISTS settings (radius INTEGER, search TEXT, price INTEGER, location TEXT, date TEXT, userID INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS events (url TEXT, name TEXT, start TEXT, end TEXT, description TEXT, userID INTEGER)")
    c.execute("CREATE TABLE IF NOT EXISTS places (radius INTEGER, search TEXT, price INTEGER, location TEXT, userID INTEGER)")
    db.commit()
    db.close()

def getUserID(user):
    db = sql.connect(DATA)
    c = db.cursor()
    data = c.execute("SELECT userID FROM accounts WHERE username = ?", (user,))
    userID = data.fetchone()[0]
    return userID

#Insert a favorited event/place into database
def addEvent(url,name,start,end,description,user):
    db = sql.connect(DATA)
    c = db.cursor()
    userID = getUserID(user)
    data = c.execute("SELECT name FROM events WHERE userID = ?", (userID,))
    exists = data.fetchall()
    if exists:
        entry = exists[0]
        for e in entry:
            if e == name:
                return 0
            else:
                c.execute("INSERT INTO events VALUES(?,?,?,?,?,?)", (url,name,start,end,description,userID,))
    else:
        c.execute("INSERT INTO events VALUES(?,?,?,?,?,?)", (url,name,start,end,description,userID,))
    db.commit()
    db.close()
    

#Gets current user's events
def getEvent(user):
    db = sql.connect(DATA)
    c = db.cursor()
    userID = getUserID(user)
    data = c.execute("SELECT * FROM events WHERE userID = ?", (userID,))
    events = data.fetchall()
    return events

#Allows users to update their preferences
def changePrefs(radius,search,price,location,date,user):
    db = sql.connect(DATA)
    c = db.cursor()
    userID = getUserID(user)
    exists = c.execute("SELECT 1 FROM settings WHERE userID = ?", (userID,))
    exist = exists.fetchall()
    if len(exist) != 0:
        c.execute("UPDATE settings SET radius=?, search=?, price=?, location=?, date=? WHERE userID = ?", (radius,search,price,location,date,userID,))
    else:
        c.execute("INSERT INTO settings VALUES(?,?,?,?,?,?)", (radius,search,price,location,date,userID,))
    db.commit()
    db.close()
    
#Gets the user's preferences 
def getUserPrefs(user):
    db = sql.connect(DATA)
    c = db.cursor()
    userID = getUserID(user)
    data = c.execute("SELECT * FROM settings WHERE userID = ?", (userID,))
    prefs = data.fetchall()
    if len(prefs) > 0:
        return prefs[0]
    else:
        return ("","","","","",0,)

def register(username, password):
    hashpass = hashlib.sha224(password).hexdigest()
    creds = (username,hashpass,)
    db = sql.connect(DATA)
    c = db.cursor()
    users = c.execute("SELECT username FROM accounts WHERE username = ?", (username,))
    if len(c.fetchall()) == 0 and len(password) >= 3:
        c.execute("INSERT INTO accounts (username,password) VALUES (?,?)", creds)
        db.commit()
        return True
    else:
        return False
    
def login(username,password):
    hashpass = hashlib.sha224(password).hexdigest()
    db = sql.connect(DATA)
    c = db.cursor()
    users = c.execute("SELECT password FROM accounts WHERE username = ?", (username,))
    data = users.fetchall()
    if len(data) == 0:
        return False
    elif data[0][0] == hashpass:
        return True
    db.commit()

def changePass(username,oldpass,newpass):
    hashnewpass = hashlib.sha224(newpass).hexdigest()
    db = sql.connect(DATA)
    c = db.cursor()
    exists = login(username,oldpass)
    if exists:
        c.execute("UPDATE accounts SET password = ? WHERE username = ?", (hashnewpass,username,))
        db.commit()
        return True
    else:
        return False


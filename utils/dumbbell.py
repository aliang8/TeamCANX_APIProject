import sqlite3 as sql
import hashlib

#CONNECT DATABASE
DATA = "data/dumbbell.db"

#Initialize databases. Only works once.
def initializeTables():
    db = sql.connect(DATA)
    c = db.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS accounts (username TEXT NOT NULL, password TEXT NOT NULL, userID INTEGER PRIMARY KEY autoincrement)")
    c.execute("CREATE TABLE IF NOT EXISTS settings (radius INTEGER, category TEXT, search TEXT, price INTEGER, location TEXT, date TEXT, userID INTEGER)")
    db.commit()
    db.close()

#Allows users to update their preferences
def changePrefs(radius, category, search, price, location, date, user):
    db = sql.connect(DATA)
    c = db.cursor()
    data = c.execute("SELECT userID FROM accounts WHERE username = ?", (user,))
    userID = data.fetchone()[0]
    exists = c.execute("SELECT 1 FROM settings WHERE userID = ?", (userID,))
    exist = exists.fetchall()
    if len(exist) != 0:
        c.execute("UPDATE settings SET radius=?, category=?, search=?, price=?, location=?, date=? WHERE userID = ?", (radius,category,search,price,location,date,userID,))
    else:
        c.execute("INSERT INTO settings VALUES(?,?,?,?,?,?,?)", (radius,category,search,price,location,date,userID,))
    db.commit()
    db.close()
    
#Gets the user's preferences 
def getUserPrefs(user):
    db = sql.connect(DATA)
    c = db.cursor()
    data = c.execute("SELECT userID FROM accounts WHERE username = ?", (user,))
    userID = data.fetchone()[0]
    data = c.execute("SELECT * FROM settings WHERE userID = ?", (userID,))
    prefs = data.fetchall()
    return prefs[0]

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


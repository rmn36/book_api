import os
import sqlite3

from cryptography.fernet import Fernet
from flask import Flask, redirect, request
from sqlite3 import Error

app = Flask(__name__)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

@app.route('/')
def hello():
    return redirect("http://www.github.com/rmn36", code=302)

@app.route('/create_user', methods=['POST'])
def create_user():
    content = request.get_json()

    connection = sqlite3.connect("book_wishlist.db")
    cursor = connection.cursor()

    res = get_user_db(connection, cursor, content)

    if (res == None):
        print("INSERT USER: "+content["email"])
        format_str = """INSERT INTO Users (email, first_name, last_name, password) VALUES ("{email}", "{first}", "{last}", "{pw}");"""
        #Encrypt password using pregenerated key
        ciphered_pw = cipher_suite.encrypt(bytes(content["password"], 'utf-8'))
        insert_cmd = format_str.format(email=content["email"], first=content["first_name"], last=content["last_name"], pw=ciphered_pw)
        cursor.execute(insert_cmd)
        ret = "CREATE USER: "+content["email"]

    connection.commit()
    connection.close()
    return ret, 201

@app.route('/update_user', methods=['PUT'])
def update_user():
    content = request.get_json()

    connection = sqlite3.connect("book_wishlist.db")
    cursor = connection.cursor()

    res = get_user_db(connection, cursor, content)

    if (res != None):
        res = update_user_db(connection, cursor, content)
     else:
        return None, 404

    connection.commit()
    connection.close()

    return res

def update_user_db(connection, cursor, content):
    print("UPDATE USER: "+content["email"])

    format_str = """UPDATE Users SET first_name = "{first}", last_name = "{last}", password = "{pw}" WHERE email = "{email}";"""
    insert_cmd = format_str.format(first=content["first_name"], last=content["last_name"], pw=content["password"], email=content["email"])

    try:
        cursor.execute(insert_cmd)
        res = "UPDATE USER: "+content["email"]
    except Error as e:
        res = str(e)
    
    return res

@app.route('/get_user/<user_email>', methods=['GET'])
def get_user(user_email):
    connection = sqlite3.connect("book_wishlist.db")
    cursor = connection.cursor()

    res = get_user_db(connection, cursor, user_email)

    connection.commit()
    connection.close()

    if(res != None):
        return str(res)
    else:
        return str(res), 404
    

def get_user_db(connection, cursor, user_email):
    format_str = """SELECT * FROM Users WHERE email="{email}" """
    get_user_cmd = format_str.format(email=user_email)
    cursor.execute(get_user_cmd)

    try:
        res = cursor.fetchone() #should only be 1 due to primary key
        if (res != None):
            res = res[:-1]
    except Error as e:
        res = e

    return res

@app.route('/create_book', methods=['POST'])
def create_book():
    content = request.get_json()

    connection = sqlite3.connect("book_wishlist.db")
    cursor = connection.cursor()

    res = get_book_db(connection, cursor, content["isbn"])

    if (res == None):
        format_str = """INSERT INTO Books (isbn, title, author, pub_date) VALUES ("{isbn}", "{title}", "{author}", "{pub_date}");"""
        insert_cmd = format_str.format(isbn=content["isbn"], title=content["title"], author=content["author"], pub_date=content["pub_date"])

        try:
            cursor.execute(insert_cmd)
            res = "CREATE BOOK: "+content["title"]
        except Error as e:
            res = str(e)
        
    connection.commit()
    connection.close()
    return res, 201

@app.route('/update_book', methods=['PUT'])
def update_book():
    content = request.get_json()

    connection = sqlite3.connect("book_wishlist.db")
    cursor = connection.cursor()

    res = get_book_db(connection, cursor, content["isbn"])

    if (res != None):
        format_str = """UPDATE Books SET title = "{title}", author = "{author}", pub_date = "{pub_date}" WHERE isbn = "{isbn}";"""
        insert_cmd = format_str.format(title=content["title"], author=content["author"], pub_date=content["pub_date"], isbn=content["isbn"])
        
        try:
            cursor.execute(insert_cmd)
            res = "UPDATE BOOK: "+content["title"]
        except Error as e:
            res = str(e)
    else:
        return None, 404

    connection.commit()
    connection.close()
    return res

@app.route('/get_book/<isbn>', methods=['GET'])
def get_book(isbn):
    connection = sqlite3.connect("book_wishlist.db")
    cursor = connection.cursor()

    res = get_book_db(connection, cursor, isbn)
    connection.commit()
    connection.close()

    if(res != None):
        return str(res)
    else:
        return str(res), 404

def get_book_db(connection, cursor, isbn):
    format_str = """SELECT * FROM Books WHERE isbn="{isbn}" """
    get_book_cmd = format_str.format(isbn=isbn)

    cursor.execute(get_book_cmd)
    res = cursor.fetchone() #should only be 1 due to primary key

    return res

@app.route('/add_to_wishlist', methods=['POST'])
def add_to_wishlist():
    content = request.get_json()

    connection = sqlite3.connect("book_wishlist.db")
    cursor = connection.cursor()

    # notes is optional
    if ("notes" in content):
        format_str = """INSERT OR IGNORE INTO Wishlist (user_email, isbn, notes) VALUES ("{user_email}", "{isbn}", "{notes}");"""
        insert_cmd = format_str.format(user_email=content["user_email"], isbn=content["isbn"], notes=content["notes"])
    else:
        format_str = """INSERT OR IGNORE INTO Wishlist (user_email, isbn) VALUES ("{user_email}", "{isbn}");"""
        insert_cmd = format_str.format(user_email=content["user_email"], isbn=content["isbn"])

    try:
        cursor.execute(insert_cmd)
        res = "ADDED "+content["isbn"]+" TO USER "+content["user_email"]+" WISHLIST"
    except Error as e:
        res = str(e)

    connection.commit()
    connection.close()
    return res, 201

@app.route('/update_wishlist', methods=['PUT'])
def update_wishlist():
    content = request.get_json()

    connection = sqlite3.connect("book_wishlist.db")
    cursor = connection.cursor()

    format_str = """SELECT * FROM Wishlist WHERE user_email="{user_email}" AND isbn="{isbn}";"""
    select_cmd = format_str.format(user_email=content["user_email"], isbn=content["isbn"])
    cursor.execute(select_cmd)
    select_result = cursor.fetchone() 

    if (select_result == None):
        return None, 404

    # notes is optional
    if ("notes" in content):
        format_str = """UPDATE Wishlist SET notes="{notes}" WHERE user_email="{user_emaik}" AND isbn="{isbn}";"""
        insert_cmd = format_str.format(user_email=content["user_email"], isbn=content["isbn"], notes=content["notes"])
    else:
        pass #notes is the only updateable content

    try:
        cursor.execute(insert_cmd)
        res = "UPDATED "+content["isbn"]+" IN USER "+content["user_email"]+" WISHLIST"
    except Error as e:
        res = str(e)

    connection.commit()
    connection.close()
    return res, 200

@app.route('/delete_wishlist_item', methods=['DELETE'])
def delete_wishlist_item():
    content = request.get_json()

    connection = sqlite3.connect("book_wishlist.db")
    cursor = connection.cursor()

    format_str = """SELECT * FROM Wishlist WHERE user_email="{user_email}" AND isbn="{isbn}";"""
    select_cmd = format_str.format(user_email=content["user_email"], isbn=content["isbn"])
    cursor.execute(select_cmd)
    select_result = cursor.fetchone() 

    if (select_result == None):
        return None, 404

    format_str = """DELETE FROM Wishlist WHERE user_email="{user_emaik}" AND isbn="{isbn}";"""
    delete_cmd = format_str.format(user_email=content["user_email"], isbn=content["isbn"])

    try:
        cursor.execute(delete_cmd)
        res = "DELETED "+content["isbn"]+" IN USER "+content["user_email"]+" WISHLIST"
    except Error as e:
        res = str(e)

    connection.commit()
    connection.close()
    return res, 200

@app.route('/delete_wishlist/<user_email>', methods=['DELETE'])
def delete_wishlist(user_email):
    content = request.get_json()

    connection = sqlite3.connect("book_wishlist.db")
    cursor = connection.cursor()

    format_str = """SELECT * FROM Wishlist WHERE user_email="{user_email}";"""
    select_cmd = format_str.format(user_email=user_email)
    cursor.execute(select_cmd)
    select_result = cursor.fetchone() 

    if (select_result == None):
        return None, 404

    format_str = """DELETE FROM Wishlist WHERE user_email="{user_emaik}";"""
    delete_cmd = format_str.format(user_email=user_email)

    try:
        cursor.execute(delete_cmd)
        res = "DELETED USER "+user_email+" WISHLIST"
    except Error as e:
        res = str(e)

    connection.commit()
    connection.close()
    return res, 200

@app.route('/get_wishlist/<user_email>', methods=['GET'])
def get_wishlist(user_email):
    content = request.get_json()

    connection = sqlite3.connect("book_wishlist.db")
    cursor = connection.cursor()

    # Get the wishlist for a user
    format_str = """SELECT * FROM Wishlist WHERE user_email="{user_email}";"""
    select_cmd = format_str.format(user_email=user_email)
    cursor.execute(select_cmd)

    res = cursor.fetchall() 

    connection.commit()
    connection.close()

    if (res != None):
        return str(res)
    else:
        return str(res), 404
    

def setup_db():
    connection = sqlite3.connect("book_wishlist.db")
    cursor = connection.cursor()

    foreign_keys = """PRAGMA foreign_keys = ON;"""
    cursor.execute(foreign_keys)
    connection.commit()

    # Create User Table
    create_user_table = """
    CREATE TABLE IF NOT EXISTS Users ( 
    email VARCHAR(50) PRIMARY KEY, 
    first_name VARCHAR(30), 
    last_name VARCHAR(30), 
    password VARCHAR(200));"""
    cursor.execute(create_user_table)

    insert_root_user = """INSERT OR IGNORE INTO Users (email, first_name, last_name, password)
    VALUES ("root", "root", "root", "root");"""
    cursor.execute(insert_root_user)

    # Create Book Table
    create_book_table = """
    CREATE TABLE IF NOT EXISTS Books ( 
    isbn VARCHAR(13) PRIMARY KEY, 
    title VARCHAR(30), 
    author VARCHAR(30), 
    pub_date DATE);"""
    cursor.execute(create_book_table)

    # Create Wishlist Table
    create_wishlist_table = """
    CREATE TABLE IF NOT EXISTS Wishlist ( 
    user_email email VARCHAR(50),
    isbn VARCHAR(13),
    date_added DATE DEFAULT (datetime('now','localtime')),
    notes TEXT,
    FOREIGN KEY(user_email) REFERENCES Users(email),
    FOREIGN KEY(isbn) REFERENCES Books(isbn),
    PRIMARY KEY (user_email, isbn));"""
    cursor.execute(create_wishlist_table)

    connection.commit()
    connection.close()

if __name__ == '__main__':
    setup_db()

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
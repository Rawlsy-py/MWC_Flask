import sqlite3

# open database
conn = sqlite3.connect('database.db')

# create table users
conn.execute('''CREATE TABLE users
            (userId INTEGER PRIMARY KEY,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            address1 TEXT,
            address2 TEXT,
            city TEXT,
            county TEXT,
            postcode TEXT,
            country TEXT,
            phone TEXT,
            )''')

# create table products
conn.execute('''CREATE TABLE products
            (productId INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT,
            dimensions TEXT,
            image TEXT,
            stock INTEGER NOT NULL,
            categoryId INTEGER,
            FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
            )''')

# create table cart
conn.execute('''CREATE TABLE cart
             (userId INTEGER,
             productId INTEGER,
             FOREIGN KEY(userId) REFERENCES users(userId),
             FOREIGN KEY(productId) REFERENCES products(productId)
             )''')

# create table categories
conn.execute('''CREATE TABLE categories
             (categoryId INTEGER PRIMARY KEY,
             name TEXT NOT NULL
             )''')

conn.close()

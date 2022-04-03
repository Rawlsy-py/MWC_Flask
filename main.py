import os
import sqlite3

import flask_login
from flask import *
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super secret key'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# login page
def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT userId, firstName FROM users WHERE email = ?", (session['email'],))
            userId, firstName = cur.fetchone()
            cur.execute("SELECT count(productId) FROM cart WHERE userId = ?", (userId,))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems)


# home page
@app.route("/")
def root():
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT productId, name, price, description, image, stock FROM products")
        itemData = cur.fetchall()
        cur.execute("SELECT categoryId, name FROM categories")
        categories = cur.fetchall()
    conn.close()
    itemData = parse(itemData)
    return render_template('home.html', itemData=itemData, categories=categories, loggedIn=loggedIn,
                           firstName=firstName, noOfItems=noOfItems)


# add
@app.route("/add")
def admin()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT categoryId, name FROM categories")
        categories = cur.fetchall()
    conn.close()
    return render_template('add.html', categories=categories)


# add item
@app.route("/addItem", methods=['GET', 'POST'])
def addItem():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category = request.form['category']
        description = request.form['description']
        stock = request.form['stock']
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO products (name, price, categoryId, description, stock) VALUES (?, ?, ?, ?, ?)",
                        (name, price, category, description, stock))
            conn.commit()
        conn.close()
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('root'))


# add category
@app.route("/addCategory", methods=['GET', 'POST'])
def addCategory():
    if request.method == 'POST':
        name = request.form['name']
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            conn.commit()
        conn.close()
        return redirect(url_for('root'))


# login
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# cart
@app.route("/cart")
def cart():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            return redirect(url_for('login'))
        else:
            cur.execute("SELECT userId FROM users WHERE email = ?", (session['email'],))
            userId = cur.fetchone()[0]
            cur.execute(
                "SELECT products.productId, name, price, quantity FROM products, cart WHERE cart.userId = ? AND cart.productId = products.productId",
                (userId,))
            products = cur.fetchall()
        conn.close()
    products = parse(products)
    return render_template('cart.html', products=products)


# remove from cart
@app.route("/removeFromCart")
def removeFromCart():
    productId = request.args.get('productId')
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            return redirect(url_for('login'))
        else:
            cur.execute("SELECT userId FROM users WHERE email = ?", (session['email'],))
            userId = cur.fetchone()[0]
            cur.execute("DELETE FROM cart WHERE userId = ? AND productId = ?", (userId, productId))
            conn.commit()
        conn.close()
    return redirect(url_for('cart'))


# checkout
@app.route("/checkout")
def checkout():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            return redirect(url_for('login'))
        else:
            cur.execute("SELECT userId FROM users WHERE email = ?", (session['email'],))
            userId = cur.fetchone()[0]
            cur.execute(
                "SELECT products.productId, name, price, quantity FROM products, cart WHERE cart.userId = ? AND cart.productId = products.productId",
                (userId,))
            products = cur.fetchall()
        conn.close()
    products = parse(products)
    return render_template('cart.html', products=products)


if __name__ == "__main__":
    app.run(debug=True)

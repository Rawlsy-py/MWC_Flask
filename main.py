import os
import sqlite3
from flask import *

app = Flask(__name__)

# app routes base
@app.route('/')
def index():
    title = "Home"
    description = "Welcome to the home page"
    return render_template('index.html', title=title, description=description)

# debug line - set false for production
if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, redirect, request, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import hashlib

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///URL.db'
# db = SQLAlchemy(app)

# class URL(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     original_url = db.Column(db.String(200))
#     short_url = db.Column(db.String(10), unique=True)

connect = sqlite3.connect('URL.db') 
connect.execute( 
    '''CREATE TABLE IF NOT EXISTS URL (original_url TEXT, short_url TEXT)''') 


@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']
    short_url = shorten_url(original_url)
    return redirect(f'/result/{short_url}')

def shorten_url(original_url):
    hash_object = hashlib.sha1(original_url.encode())
    hex_dig = hash_object.hexdigest()[:8]
    # new_url = URL(original_url=original_url, short_url=hex_dig)
    # db.session.add(new_url)
    # db.session.commit()
    with sqlite3.connect('URL.db') as urls:
        cur=urls.cursor()
        print(original_url,"    PRINT HO RAHI HAI    ",hex_dig)
        cur.execute("INSERT INTO URL (original_url,short_url) values (?, ?)",(original_url,hex_dig))
        
        urls.commit()


        
    return hex_dig

def fetch_url(short_url):
    con=sqlite3.connect('URL.db')
    cur=con.cursor()
    db_original_url=cur.execute("SELECT original_url from URL where short_url== ?",(short_url,)).fetchone()
    if len(db_original_url) ==0:
        return None

    print(db_original_url)
    return db_original_url[0]
    

@app.route('/<short_url>')
def redirect_to_url(short_url):
    original_url = fetch_url(short_url)
    if original_url:
        # original_url = url_mapping.original_url
        return redirect(original_url)
    else:
        return "Shortened URL not found", 404

@app.route('/result/<short_url>')
def redirect_to_url_page(short_url):
    original_url = fetch_url(short_url)
    if original_url:
        # original_url = url_mapping.original_url
        return render_template('result2.html', original_url=original_url, short_url=short_url)
    else:
        return "Shortened URL not found", 404

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except:
        print("krishna is noob")
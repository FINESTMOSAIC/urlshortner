from flask import Flask, redirect, request,render_template
from flask_sqlalchemy import SQLAlchemy
import hashlib



app = Flask(__name__)
# Replace the below URI with your MySQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:25dec2002@FinestMosaic69/url'
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(200), unique=True)
    short_url = db.Column(db.String(10), unique=True)

@app.route('/')
# def index():
#     return 'Welcome to the URL Shortener!'

def index():
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']  # Extract the original URL from the form data
    short_url = shorten_url(original_url)  # Call the shorten_url function with the original URL
    # return short_url  # Return the shortened URL as the response
    return redirect(f'/result/{short_url}')
# def shorten_url():
#     original_url = request.form['url']
#     # Shortening logic here
#     # Save original_url and short_url in the database
#     return 'Shortened URL'

# def shorten_url(original_url):
#     # Apply a hashing algorithm to generate a unique short identifier
#     hash_object = hashlib.sha1(original_url.encode())
#     hex_dig = hash_object.hexdigest()[:8]  # Using first 8 characters as the short URL
#     return hex_dig

def shorten_url(original_url):
    # Apply a hashing algorithm to generate a unique short identifier
    hash_object = hashlib.sha1(original_url.encode())
    hex_dig = hash_object.hexdigest()[:8]  # Using first 8 characters as the short URL
    
    # Create a new URL instance
    new_url = URL(original_url=original_url, short_url=hex_dig)
    
    # Add the new URL instance to the session
    db.session.add(new_url)
    
    # Commit the changes to the database
    db.session.commit()
    
    # Return the short URL
    return hex_dig



# @app.route('/<short_url>')
# def redirect_to_url(short_url):
#     # Retrieve original_url from the database using short_url
#     original_url = URL.query.filter_by(short_url=short_url).first().original_url
#     return redirect(original_url)

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url_mapping = URL.query.filter_by(short_url=short_url).first()
    if url_mapping:
        original_url = url_mapping.original_url
        return redirect(original_url)
    else:
        return "Shortened URL not found", 404


@app.route('/result/<short_url>')

def redirect_to_url_page(short_url):
    # Retrieve the original URL from the database based on the short URL
    url_mapping = URL.query.filter_by(short_url=short_url).first()
    if url_mapping:
        original_url = url_mapping.original_url
        # return redirect(original_url)
        return render_template('result.html', original_url=original_url, short_url=short_url)
    else:
        return "Shortened URL not found", 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

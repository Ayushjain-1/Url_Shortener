from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Model
class Urls(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(), unique=True)
    short_url = db.Column(db.String(6), unique=True)

    def __init__(self, long_url, short_url):
        self.long_url = long_url
        self.short_url = short_url

def create_tables():
    with app.app_context():
        db.create_all()

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(3))
    return short_url

@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        long_url = request.form.get("long_url")

        # Check if the long URL is already in the database
        url_entry = Urls.query.filter_by(long_url=long_url).first()

        if url_entry:
            return render_template("result.html", short_url=url_entry.short_url)

        # Generate a new short URL
        short_url = generate_short_url()

        # Create a new database entry
        new_url = Urls(long_url=long_url, short_url=short_url)
        db.session.add(new_url)
        db.session.commit()

        return render_template("result.html", short_url=short_url)
    else:
        return render_template("home.html")

@app.route('/<short_url>')
def redirect_to_long_url(short_url):
    url_entry = Urls.query.filter_by(short_url=short_url).first()
    if url_entry:
        return redirect(url_entry.long_url)
    else:
        return "URL not found."

if __name__ == '__main__':
    create_tables()  # Call the create_tables function
    app.run(port=5000, debug=True)

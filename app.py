import configuration

import datetime
import os

from flask import Flask, render_template, flash, sessions
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
res = configuration.Response()

app.secret_key = "37821acf98b1e749b237e6a976e93fb0"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

comment_made = db.Table('comment_made',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.comment_id'), primary_key=True)
)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    date_registered = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    commenting = db.relationship('Comment', secondary=comment_made)

    def __repr__(self):
        return f'<{self.user_id} - {self.firstname}>'

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer)
    comment = db.Column(db.String(500))
    time_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<{self.comment_id} - {self.movie_id}>'

if os.path.exists('data.sqlite3') == False: db.create_all()

@app.route('/')
def index():
    top_rated = res.get_top_rated_movies()
    popular_movies = res.get_popular_movies()
    return render_template('index.html',
                           top_rated = top_rated, popular_movies = popular_movies)

@app.route('/details/<movie_id>')
def details(movie_id: int):
    movie_details = res.get_movie_details_by_id(int(movie_id))
    movie_trailer_key = res.get_trailer_by_id(movie_id)
    return render_template('details.html',
                           movie_details = movie_details, movie_key = movie_trailer_key)

@app.route('/process', methods=['POST', 'GET'])
def process():
    pass

if __name__ == '__main__':
    app.run(debug=True)

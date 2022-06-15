from curses import meta
import configuration
from forms import Registration, Login, CommentField

import datetime
import os

from flask import Flask, render_template, flash, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
res = configuration.Response()

app.secret_key = "37821acf98b1e749b237e6a976e93fb0"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = datetime.timedelta(minutes=30)

db = SQLAlchemy(app)

# Database relationship. Many To Many relationship.
comment_made = db.Table('comment_made',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('comment_id', db.Integer, db.ForeignKey('comment.comment_id'), primary_key=True)
)

# User table
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    password = db.Column(db.String(255))
    date_registered = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    commenting = db.relationship('Comment', secondary=comment_made)

    def __repr__(self):
        return f'<{self.user_id} - {self.first_name}>'

# Comment table
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

@app.route('/details/<movie_id>', methods=['GET', 'POST'])
def details(movie_id: int):
    form = CommentField()

    movie_details = res.get_movie_details_by_id(int(movie_id))
    movie_trailer_key = res.get_trailer_by_id(movie_id)
    
    if request.method == 'POST':
        # Code for commenting logic
        # movie id is movie_id parameter
        # comment_id is auto generated
        if form.comment_written.data.strip() == '': return redirect(url_for('details', movie_id=movie_id))
        
        user = User.query.filter_by(email=session['email']).first()
        comment = Comment(movie_id=movie_id, comment=form.comment_written.data)
        db.session.add(comment)
        db.session.commit()
        
        user.commenting.append(comment)
        db.session.commit()
        
        return redirect(url_for('details', movie_id=movie_id))

    else:
        display_comments = list(db.engine.execute(f"""                                                               
                                    SELECT email, comment, datetime(time_added), c.comment_id
                                    FROM user u, comment c
                                    JOIN comment_made cm
                                        ON (u.user_id = cm.user_id) AND (c.comment_id = cm.comment_id)
                                    WHERE movie_id = {movie_id}
                                        """))
        
        return render_template('details.html',
                                movie_details = movie_details, movie_key = movie_trailer_key,
                                form=form, movie_id = movie_id, display_comments = display_comments[::-1])

@app.route('/remove_comment/<comment_id>', methods=['GET', 'POST'])
def remove_comment(comment_id: int):
    if 'email' in session:
        user = User.query.filter_by(email=session['email']).first()
        specific_comment = Comment.query.filter_by(comment_id=comment_id).first()
        user.commenting.remove(specific_comment)
        db.session.commit()
        return redirect(url_for('details', movie_id=specific_comment.movie_id))


@app.route('/process', methods=['POST', 'GET'])
def process():
    pass

# Registration handler
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = Registration()
    
    # Checking if user send post request to register
    if request.method == 'POST':
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('User with this email already exists', 'danger')
            return redirect(url_for('register'))
        
        else:
            
            user = User(email=form.data['email'], first_name=form.data['name'],
                        last_name=form.data['surname'], password=form.data['password']) # Creating an object
            
            db.session.add(user) # Adding object into database
            db.session.commit() # Saving changes
            
            flash('You are now registered and can log in.', 'success') # Giving sign of successful registration
            
            # If user is registered successfully, redirect to login page
            return redirect(url_for('login'))
    
              
    # If user sends a get requests then go to register page
    else:
        return render_template('registration.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Login()
    
    if request.method == 'POST':
        
        existing_user = User.query.filter_by(email=form.email.data).first() # Selecting an user by email
        
        # If the email selected is not in database then show error message
        if (not existing_user) or (existing_user.password != form.password.data):
            flash('Wrong email or password', 'danger')
            return redirect(url_for('login'))
        
        # If email does exists, then there are the following procedures
        else:
            session['email'] = form.email.data # Adding into session using email where key is 'email' and value if form.email.data
            return redirect(url_for('index')) # Redirect to index page
        
    else:
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))


# Additional functions

@app.route('/dark', methods=['POST', 'GET'])
def dark():
    if 'darktheme' not in session:
        session['darktheme'] = True
        print(request.url)
        return redirect(url_for('index'))
    else:
        session.pop('darktheme')
        print(request.url)
        
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

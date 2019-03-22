import os
from flask import Flask, render_template, session, redirect, url_for # tools that will make it easier to build on things
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this

# Application configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./sample_movies.db' # TODO: decide what your new database name will be -- that has to go here
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set up Flask debug stuff
db = SQLAlchemy(app) # For database use
session = db.session # to make queries easy


#########
######### Everything above this line is important/useful setup, not problem-solving.
#########


##### Set up Models #####

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))

    # Foreign keys
    director_name = db.Column(db.Integer, db.ForeignKey('directors.id'))
    genre_name = db.Column(db.Integer, db.ForeignKey('genres.id'))

    # Relationship with other classes
    director = db.relationship('Director',backref='Movie')
    genre = db.relationship('Genre', backref='Movie')

    def __repr__(self):
        return "{} (ID: {})".format(self.title, self.id)

class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name,self.id)

class Genre(db.Model):
    __tablename__ = "genres"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

##### Helper functions #####

### For database additions
### Relying on global session variable above existing

def get_or_create_director(director_name):
    director = Director.query.filter_by(name=director_name).first()
    if director:
        return director
    else:
        director = Director(name=director_name)
        session.add(director)
        session.commit()
        return director

def get_or_create_genre(genre_name):
    genre = Genre.query.filter_by(genre=genre_name).first()
    if genre:
        return genre
    else:
        genre = Genre(genre=genre_name)
        session.add(genre)
        session.commit()
        return genre

##### Set up Controllers (route functions) #####

## Main route
@app.route('/')
def index():
    movies = Movie.query.all()
    num_movies = len(movies)
    return render_template('index.html', num_movies=num_movies)

@app.route('/movie/new/<title>/<director>/<genre>/')
def new_movie(title, director, genre):
    if Movie.query.filter_by(title=title).first():
        return "That movie already exists in the database."
    else:
        director = get_or_create_director(director)
        genre = get_or_create_genre(genre)
        movie = Movie(title=title, director_name=director.name, genre_name=genre.name)
        session.add(movie)
        session.commit()
        return "New movie added to database: {} by {} - {}.".format(movie.title, director.name, genre.name)

@app.route('/all_movies')
def see_all():
    all_movies = []
    movies = Movie.query.all()
    for x in movies:
        director = Director.query.filter_by(id=x.director_name).first()
        all_movies.append((x.title, x.director_name, x.movie_id))
    return render_template('all_movies.html',all_movies=all_movies)

@app.route('/all_directors')
def see_all_artists():
    directors = Director.query.all()
    names = []
    for d in directors:
        num_movies = len(Movie.query.filter_by(director_name=d.name).all())
        newtup = (d.name, num_movies)
        names.append(newtup)
    return render_template('all_directors.html',director_names=names)

if __name__ == '__main__':
    db.create_all() # This will create database in current directory, as set up, if it doesn't exist, but won't overwrite if you restart - so no worries about that
    app.run() # run with this: python main_app.py runserver

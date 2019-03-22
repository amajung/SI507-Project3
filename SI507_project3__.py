import os
from flask import Flask, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy # handles database stuff for us - need to pip install flask_sqlalchemy in your virtual env, environment, etc to use this and run this

app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'hard to guess string for app security adgsdfsadfdflsdfsj'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./sample_movies.db'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
session = db.session

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    release_year = db.Column(db.Integer, db.ForeignKey('release_date.id'))
    director_name = db.Column(db.Integer, db.ForeignKey('directors.id'))
    release = db.relationship('Release_Date', backref='movies')
    director = db.relationship('Director',backref='movies')

    def __repr__(self):
        return "{} (ID: {})".format(self.title,self.id)

class Director(db.Model):
    __tablename__ = "directors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "{} (ID: {})".format(self.name,self.id)

class Release_Date(db.Model):
    __tablename__ = "release_date"
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)

def get_or_create_director(director_name):
    director = Director.query.filter_by(name=director_name).first()
    if director:
        return director
    else:
        director = Director(name=director_name)
        session.add(director)
        session.commit()
        return director

def get_or_create_date(year):
    date = Release_Date.query.filter_by(year=year).first()
    if date:
        return date
    else:
        date = Release_Date(year=year)
        session.add(date)
        session.commit()
        return date

@app.route('/')
def index():
    movies = Movie.query.all()
    num_movies = len(movies)
    return render_template('index.html', num_movies=num_movies)

@app.route('/movie/new/<title>/<director>/<year>/')
def new_movie(title, director, year):
    if Movie.query.filter_by(title=title).first():
        return "That movie already exists in the database."
    else:
        director = get_or_create_director(director)
        release_year = get_or_create_date(year)
        movie = Movie(title=title, director_name=director.name, release_year=release_year.year)
        session.add(movie)
        session.commit()
        return "New movie added to database: {} by {}, {}.".format(movie.title, director.name, release_year.year)

@app.route('/all_movies')
def see_all():
    all_movies = []
    movies = Movie.query.all()
    for x in movies:
        director = Director.query.filter_by(id=x.director_name).first()
        release_date = Release_Date.query.filter_by(id=x.release_year).first()
        all_movies.append((x.title, x.director_name, x.release_year))
    return render_template('all_movies.html',all_movies=all_movies)

@app.route('/all_directors')
def see_all_artists():
    directors = Director.query.all()
    names = []
    for d in directors:
        num_movies = len(Movie.query.filter_by(director_name=d.name).all())
        newtup = (d.name,num_movies)
        names.append(newtup)
    return render_template('all_directors.html',director_names=names)


if __name__ == '__main__':
    db.create_all()
app.run()

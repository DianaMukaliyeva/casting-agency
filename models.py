import os
import dateutil.parser

from sqlalchemy import Column, Integer, String, DateTime
from flask_sqlalchemy import SQLAlchemy

database_path = os.getenv('DATABASE_URL')

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    '''Binds a flask application and a SQLAlchemy service.'''

    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


# Many-to-many relationship between movies and actors
movie_actor = db.Table(
    'movie_actor',
    Column('movie_id', Integer, db.ForeignKey('movies.id'), primary_key=True),
    Column('actor_id', Integer, db.ForeignKey('actors.id'), primary_key=True)
)


class Movie(db.Model):
    '''
    Movie
    Has title and release date
    '''
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    release_date = Column(DateTime, nullable=False)
    actors = db.relationship('Actor', secondary=movie_actor, backref='movies')

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime('%A, %b %d %Y')
        }


class Actor(db.Model):
    '''
    Actor
    Has name, age and gender
    '''
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def __init__(self, name, age, gender):
        self.name = name,
        self.age = age,
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

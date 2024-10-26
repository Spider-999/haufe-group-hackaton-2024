from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    # Unique identifier for the user
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    college = db.Column(db.String(4), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    # One to many relationship, a user can have many posts
    # Refer to posts as post and load all data at once from the database
    posts = db.relationship('PartyPost', backref='user', lazy=True)
    participants = db.relationship('Participant', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy='dynamic')


class PartyPost(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(32), nullable=False)
    location = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    content = db.Column(db.Text, nullable=False)

    participants = db.relationship('Participant', backref='post', lazy=True)
    comments = db.relationship('Comment', backref='post', cascade='all, delete-orphan', lazy='dynamic')


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    time_posted = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
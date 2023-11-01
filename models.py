import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://res.cloudinary.com/graham-media-group/image/upload/f_auto/q_auto/c_scale,w_500/v1/media/gmg/2SOUM4AVRJC75O6LRHU2XU7M6M.jpg?_a=AJFJtWIA"

class User(db.Model):
    """Site user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")


class Post(db.Model):
    """Posts"""

    __tablename__ = "Posts"

    id = db.Column(db.Interger, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(default=datetime.datetime.now)
    user_id = db.Column(db.Interger, db.ForeignKey('users.id'), nullable=False)


class PostTag(db.model):
    """Tags on posts"""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'),primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.model):
    """Tag that can be added to post """

    __tablename__ = "tags"

    id = db.Column(db.Interger, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    post = db.relationship('Posts', secondary="post_tags", cascade="all, delete", backref="tags") 


def connect_db(app):
    db.app = app
    db.init_app(app)
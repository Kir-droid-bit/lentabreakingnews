from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import ForeignKey
from app import app

db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


class Users(db.Model):
    __table_name__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(),unique=True)
    password = db.Column(db.String())
    time = db.Column(db.DateTime())
    comments = db.relationship('Comment',backref='owner')
    def __str__(self):
        return 'Database is create.'
class Comment(db.Model):
    __table_name__ = " Comments "
    id = db.Column(db.Integer,primary_key=True)
    login = db.Column(db.String,nullable = False)
    comment = db.Column(db.String(),nullable=False)
    post_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, ForeignKey('users.id'))
    def __str__(self):
        return 'Database is create'

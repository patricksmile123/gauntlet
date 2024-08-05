from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .db import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False, index=True)
    lastname = db.Column(db.String(20), nullable=False, index=True)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    db.relationship('Game', backref='user_id', lazy='dynamic')
    
    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password, salt_length=32)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class Game(db.Model):
    __tablename__ = 'games'
    game_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    outcome = db.Column(db.String(10), nullable=True)
    answer = db.Column(db.String(10), nullable=False)

class WordleGuess(db.Model):
    __tablename__ = 'wordle_guess'
    guess_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    guess = db.Column(db.String(10), nullable=False)
    guess_time = db.Column(db.DateTime, nullable=False)



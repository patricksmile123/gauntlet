from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from db import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False, index=True)
    lastname = db.Column(db.String(20), nullable=False, index=True)
    username = db.Column(db.String(20), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    games = db.relationship('Game', backref='user', lazy='dynamic')
    achievements = db.relationship('UserAchievement', back_populates='user', lazy='dynamic')

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
    score = db.Column(db.Integer, nullable=True)

class WordleGuess(db.Model):
    __tablename__ = 'wordle_guess'
    guess_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    guess = db.Column(db.String(10), nullable=False)
    guess_time = db.Column(db.DateTime, nullable=False)

class Achievement(db.Model):
    __tablename__ = 'achievements'
    achievement_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    requirement = db.Column(db.String(200), nullable=True)
    user_achievements = db.relationship('UserAchievement', back_populates='achievement', lazy='dynamic')

class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.achievement_id'), nullable=False)
    date_achieved = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', back_populates='achievements')   
    achievement = db.relationship('Achievement', back_populates='user_achievements')

class SharedGame(db.Model):
    __tablename__= 'shared_game'
    sharedGameID = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    uuid = db.Column(db.String(36), nullable=False)
    answer = db.Column(db.String(10), nullable=False)

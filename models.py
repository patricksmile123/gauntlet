from db import db

class Game(db.Model):
    __tablename__ = 'transient_games'
    game_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    outcome = db.Column(db.String(10), nullable=True)
    answer = db.Column(db.String(10), nullable=False)
    score = db.Column(db.Integer, nullable=True)

class WordleGuess(db.Model):
    __tablename__ = 'transient_wordle_guess'
    guess_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('transient_games.game_id'), nullable=False)
    guess = db.Column(db.String(10), nullable=False)
    guess_time = db.Column(db.DateTime, nullable=False)

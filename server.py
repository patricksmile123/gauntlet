from ast import parse
from flask import Flask, request, jsonify, send_from_directory
import random
from models import User, Game, WordleGuess, Achievement, UserAchievement
from application import app
from forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
import jwt
from datetime import datetime
import traceback
from sqlalchemy import text

# Sample word list
WORD_LIST = open("wordle_words.txt").read().splitlines()
LEADERBOARD_QUERY = open("leaderboard.sql").read()

def parseResult(guess, answer):
    result = []
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            result.append('correct')
        elif guess[i] in answer:
            result.append('present')
        else:
            result.append('absent')
    return result

@app.route('/api/createGame', methods=['GET'])
def createGame():
    authoHeader = request.headers.get('authorization')
    token = authoHeader.split(" ")[1]
    try:
        decodedJwt = jwt.decode(token, "s{$822Qcg!d*", algorithms=["HS256"])
        user = User.query.filter_by(username=decodedJwt['username']).first()
        currentGame = Game.query.filter_by(user_id=user.user_id).filter_by(outcome=None).order_by(Game.game_id.desc()).first()
        if currentGame == None:
            newGame = Game(
                user_id=user.user_id,
                start_time=datetime.now(),
                answer=random.choice(WORD_LIST)
            )
            db.session.add(newGame)
            db.session.commit()
            return jsonify(newGame.game_id)
        else:
            currentGuesses = WordleGuess.query.filter_by(game_id = currentGame.game_id).order_by(WordleGuess.guess_time.asc()).all()
            currentGuesses = [{"guess": guess.guess, "result": parseResult(guess.guess, currentGame.answer)} for guess in currentGuesses]
            return jsonify(currentGuesses)

    except:
        print(traceback.format_exc())
        return jsonify({"error": "Invalid token"}), 400
    
def check_achievements(user, currentGame):

    current_achievements = {ach.achievement_id for ach in UserAchievement.query.filter_by(user_id=user.user_id).all()}
    all_achievements = Achievement.query.all()
    new_achievements = []
    
    total_wins = Game.query.filter_by(user_id=user.user_id, outcome='win').count()
    
    total_losses = Game.query.filter_by(user_id=user.user_id, outcome='loss').count()
    scores = [game.score for game in Game.query.filter_by(user_id=user.user_id) if game.score]
    avg_score = sum(scores) / len(scores) if scores else 0
    times = [(game.end_time - game.start_time).total_seconds() for game in Game.query.filter_by(user_id=user.user_id) if game.end_time]
    avg_time = sum(times) / len(times) if times else 0
    
    game_time = (currentGame.end_time - currentGame.start_time).total_seconds() if currentGame.end_time else 0

    for achievement in all_achievements:
        if achievement.achievement_id in current_achievements:
            continue
        if achievement.name == 'First Login':
            new_achievements.append(achievement)
        elif achievement.name == 'First Win' and total_wins >= 1:
            new_achievements.append(achievement)
        elif achievement.name == 'Win 10 Games' and total_wins >= 10:
            new_achievements.append(achievement)
        elif achievement.name == 'Win 100 Games' and total_wins >= 100:
            new_achievements.append(achievement)
        elif achievement.name == 'Win 250 Games' and total_wins >= 250:
            new_achievements.append(achievement)
        elif achievement.name == 'Win 500 Games' and total_wins >= 500:
            new_achievements.append(achievement)
        elif achievement.name == 'Win 1000 Games' and total_wins >= 1000:
            new_achievements.append(achievement)
        elif achievement.name == 'First Loss' and total_losses >= 1:
            new_achievements.append(achievement)
        elif achievement.name == 'Lose 10 Games' and total_losses >= 10:
            new_achievements.append(achievement)
        elif achievement.name == 'Lose 100 Games' and total_losses >= 100:
            new_achievements.append(achievement)
        elif achievement.name == 'Win a game in 60 seconds' and currentGame.outcome == 'win' and game_time <= 60:
            new_achievements.append(achievement)
        elif achievement.name == 'Win a game in 30 seconds' and currentGame.outcome == 'win' and game_time <= 30:
            new_achievements.append(achievement)
        elif achievement.name == 'Win a game in 15 seconds' and currentGame.outcome == 'win' and game_time <= 15:
            new_achievements.append(achievement)
        elif achievement.name == 'Average time of 5 minutes' and avg_time <= 300:
            new_achievements.append(achievement)
        elif achievement.name == 'Average time of 3 minutes' and avg_time <= 180:
            new_achievements.append(achievement)
        elif achievement.name == 'Average score of 5' and avg_score <= 5:
            new_achievements.append(achievement)
        elif achievement.name == 'Average score of 4.75' and avg_score <= 4.75:
            new_achievements.append(achievement)
        elif achievement.name == 'Average score of 4.5' and avg_score <= 4.5:
            new_achievements.append(achievement)
        elif achievement.name == 'Average score of 4' and avg_score <= 4:
            new_achievements.append(achievement)
        elif achievement.name == 'Average score of 3.5' and avg_score <= 3.5:
            new_achievements.append(achievement)
    
    for achievement in new_achievements:
        user_achievement = UserAchievement(
            user_id=user.user_id,
            achievement_id=achievement.achievement_id,
            date_achieved=datetime.now()
        )
        db.session.add(user_achievement)
    
    db.session.commit()

    return new_achievements



@app.route('/api/guess', methods=['POST'])
def guess():
    authoHeader = request.headers.get('authorization')
    token = authoHeader.split(" ")[1]
    try:
        decodedJwt = jwt.decode(token, "s{$822Qcg!d*", algorithms=["HS256"])
        user = User.query.filter_by(username=decodedJwt['username']).first()
        currentGame = Game.query.filter_by(user_id=user.user_id).order_by(Game.game_id.desc()).first()
        data = request.get_json()
        if not data or 'guess' not in data:
            return jsonify({"error": "Invalid input"}), 400
        guess = data['guess'].lower()
        dbGuess = WordleGuess(
            game_id=currentGame.game_id,
            guess=guess,
            guess_time=datetime.now()
        )
        db.session.add(dbGuess)
        guessCount = WordleGuess.query.filter_by(game_id=currentGame.game_id).count()
        if guess == currentGame.answer:
            currentGame.score = guessCount
            currentGame.end_time = datetime.now()
            currentGame.outcome = "win"
        elif guessCount >= len(currentGame.answer):
            currentGame.score = guessCount
            currentGame.end_time = datetime.now()
            currentGame.outcome = "loss"
        db.session.commit()
        result = parseResult(guess, currentGame.answer)
        response = {"result": result, "guessCount": WordleGuess.query.filter_by(game_id=currentGame.game_id).count(), "new_achievements": [a.name for a in check_achievements(user, currentGame)]}
        print(response)
        return jsonify(response)
    except:
        print(traceback.format_exc())
        return jsonify({"error": "Invalid token"}), 400


@app.route('/api/signup', methods=['POST'])
def signup():
    print("SIGNUP FUNCTION CALLED")
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    form = RegistrationForm(data=data)
    #print("signup", session['csrf_token'])
    if form.validate_on_submit():
        print("Form is valid")
        new_user = User(
            username=form.username.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            password_hash=generate_password_hash(form.password.data, salt_length=32)
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    else:
        errors = form.errors
        return jsonify({'errors': errors}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input"}), 400
    form = LoginForm(data=data)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user == None:
            return jsonify({"error": "User not found"}), 404
        if check_password_hash(user.password_hash, form.password.data) == False or form.password.data == None:
            return jsonify({"error": "Invalid Username or Password"}), 400
        encodedJwt = jwt.encode({"username": user.username}, "s{$822Qcg!d*", algorithm="HS256")
        return jsonify({"username": user.username, "token": encodedJwt}), 200
    
@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    leaderboardRows = db.session.execute(text(LEADERBOARD_QUERY)).fetchall()
    leaderboard = [{"firstname": row[0], "averageScore": row[1], "averageTime": row[2], "rank": row[3]} for row in leaderboardRows]
    return jsonify(leaderboard)

@app.route('/', defaults = {'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path.startswith('static/') or path.startswith('media/'):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/populate_achievements', methods=['GET'])
def populate_achievements():
    if Achievement.query.count() == 0:
        achievements = [
            Achievement(name='First Login', requirement='Login once'),
            Achievement(name='First Win', requirement='Win one Wordle game'),
            Achievement(name='Win 10 Games', requirement='Win 10 Wordle games'),
            Achievement(name='Win 100 Games', requirement='Win 100 Wordle games'),
            Achievement(name='Win 250 Games', requirement='Win 250 Wordle games'),
            Achievement(name='Win 500 Games', requirement='Win 500 Wordle games'),
            Achievement(name='Win 1000 Games', requirement='Win 1000 Wordle games'),
            Achievement(name='First Loss', requirement='Lose one Wordle game'),
            Achievement(name='Lose 10 Games', requirement='Lose 10 Wordle games'),
            Achievement(name='Lose 100 Games', requirement='Lose 100 Wordle games'),
            Achievement(name='Win a game in 60 seconds', requirement='Win a game in 60 seconds or less'),
            Achievement(name='Win a game in 30 seconds', requirement='Win a game in 30 seconds or less'),
            Achievement(name='Win a game in 15 seconds', requirement='Win a game in 15 seconds or less'),
            Achievement(name='Average time of 5 minutes', requirement='Average time of 5 minutes or less'),
            Achievement(name='Average time of 3 minutes', requirement='Average time of 3 minutes or less'),
            Achievement(name='Average score of 5', requirement='Average score of 5 or less'),
            Achievement(name='Average score of 4.75', requirement='Average score of 4.75 or less'),
            Achievement(name='Average score of 4.5', requirement='Average score of 4.5 or less'),
            Achievement(name='Average score of 4', requirement='Average score of 4 or less'),
            Achievement(name='Average score of 3.5', requirement='Average score of 3.5 or less'),
        ]

        db.session.bulk_save_objects(achievements)
        db.session.commit()


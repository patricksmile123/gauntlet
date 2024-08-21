from ast import parse
from flask import Flask, request, jsonify, send_from_directory
import random
from models import User, Game, WordleGuess, Achievement, UserAchievement, SharedGame
from application import app
from forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
import jwt
from datetime import datetime
import traceback
from sqlalchemy import text
import time
import uuid
from english_words import get_english_words_set

# Sample word list
WORD_LIST = open("wordle_words.txt").read().splitlines()
LEADERBOARD_QUERY = open("leaderboard.sql").read()
LEADERBOARD_QUERY6 = open("leaderboard6.sql").read()
LEADERBOARD_QUERY7 = open("leaderboard7.sql").read()
LEADERBOARD_QUERY8 = open("leaderboard8.sql").read()
WORD_LIST6 = open("wordle_words6.txt").read().splitlines()
WORD_LIST7 = open("wordle_words7.txt").read().splitlines()
WORD_LIST8 = open("wordle_words8.txt").read().splitlines()
ENGLISH_WORDS = get_english_words_set(['web2'], lower=True)

def parseResult(guess, answer):
    confirmed_correct = [''] * len(answer)
    result = []
    letterCount = {}

    for i in range(len(guess)):
        if guess[i] == answer[i]:
            confirmed_correct[i] = guess[i]

    for letter in answer:
        letterCount[letter] = letterCount.get(letter, 0) + 1

    for i, letter in enumerate(confirmed_correct):
        if letter:
            letterCount[letter] -= 1

    for i in range(len(guess)):
        if guess[i] == answer[i]:
            result.append('correct')
        elif guess[i] in answer and letterCount[guess[i]] > 0:
            result.append('present')
            letterCount[guess[i]] -= 1 
        else:
            result.append('absent')

    return result

@app.route('/api/createGame', methods=['GET'])
def createGame():
    authoHeader = request.headers.get('authorization')
    answer=random.choice(WORD_LIST)
    if request.headers.get('shareduuid'):
        uuid = request.headers.get('shareduuid')
        sharedGame = SharedGame.query.filter_by(uuid=uuid).first()
        if sharedGame != None:
            answer = sharedGame.answer
    
    token = authoHeader.split(" ")[1]
    try:
        decodedJwt = jwt.decode(token, "s{$822Qcg!d*", algorithms=["HS256"])
        user = User.query.filter_by(username=decodedJwt['username']).first()
        currentGames = Game.query.filter_by(user_id=user.user_id).filter_by(outcome=None).order_by(Game.game_id.desc()).all()
        currentGame = None
        for game in currentGames:
            if len(game.answer) == 5:
                currentGame = game
        if currentGame == None:
            newGame = Game(
                user_id=user.user_id,
                start_time=datetime.now(),
                answer = answer
            )
            db.session.add(newGame)
            print("Answer: " + newGame.answer)
            db.session.commit()
            return jsonify(newGame.game_id)
        else:
            currentGuesses = WordleGuess.query.filter_by(game_id = currentGame.game_id).order_by(WordleGuess.guess_time.asc()).all()
            currentGuesses = [{"guess": guess.guess, "result": parseResult(guess.guess, currentGame.answer)} for guess in currentGuesses]
            return jsonify(currentGuesses)

    except:
        print(traceback.format_exc())
        return jsonify({"error": "Invalid token"}), 400
    
@app.route('/api/createGameN', methods=['GET'])
def createGameN():
    authoHeader = request.headers.get('authorization')
    token = authoHeader.split(" ")[1]
    wordLength = request.headers.get('wordLength')
    sharedGame = None
    if request.headers.get('shareduuid'):
        uuid = request.headers.get('shareduuid')
        sharedGame = SharedGame.query.filter_by(uuid=uuid).first()

    try:
        if sharedGame != None:
            answer = sharedGame.answer
            wordLength = len(sharedGame.answer)
        elif wordLength == '6':
            answer=random.choice(WORD_LIST6)
        elif wordLength == '7':
            answer=random.choice(WORD_LIST7)
        elif wordLength == '8':
            answer=random.choice(WORD_LIST8)
        else:
            return jsonify({"error": "No shared game found"}), 404
        print(answer)
        
        decodedJwt = jwt.decode(token, "s{$822Qcg!d*", algorithms=["HS256"])
        user = User.query.filter_by(username=decodedJwt['username']).first()
        currentGames = Game.query.filter_by(user_id=user.user_id).filter_by(outcome=None).order_by(Game.game_id.desc()).all()
        currentGame = None
        for game in currentGames:
            if len(game.answer) == int(wordLength):
                currentGame = game
        if currentGame == None:
            newGame = Game(
                user_id=user.user_id,
                start_time=datetime.now(),
                answer=answer
            )
            print (answer)
            db.session.add(newGame)
            db.session.commit()
            response = {"wordLength": wordLength}   
            return jsonify(response)
        else:
            currentGuesses = WordleGuess.query.filter_by(game_id = currentGame.game_id).order_by(WordleGuess.guess_time.asc()).all()
            currentGuesses = [{"guess": guess.guess, "result": parseResult(guess.guess, currentGame.answer)} for guess in currentGuesses]
            return jsonify({"guesses": currentGuesses, "wordLength": wordLength})

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
    
    user_achievements = [UserAchievement(user_id=user.user_id, achievement_id=achievement.achievement_id, date_achieved=datetime.now()) for achievement in new_achievements]
    db.session.bulk_save_objects(user_achievements)

    return new_achievements



@app.route('/api/guess', methods=['POST'])
def guess():
    authoHeader = request.headers.get('authorization')
    token = authoHeader.split(" ")[1]
    try:
        decodedJwt = jwt.decode(token, "s{$822Qcg!d*", algorithms=["HS256"])
        user = User.query.filter_by(username=decodedJwt['username']).first()
        data = request.get_json()
        if not data or 'guess' not in data:
            return jsonify({"error": "Invalid input"}), 400
        guess = data['guess'].lower()
        # if guess not in ENGLISH_WORDS:
        #     return jsonify({"error": "Invalid guess"}), 400
        currentGames = Game.query.filter_by(user_id=user.user_id, outcome=None).order_by(Game.game_id.desc()).all()
        currentGame = None
        for game in currentGames:
            if len(game.answer) == len(guess):
                currentGame = game
        dbGuess = WordleGuess(
            game_id=currentGame.game_id,
            guess=guess,
            guess_time=datetime.now()
        )
        db.session.add(dbGuess)
        guessCount = WordleGuess.query.filter_by(game_id=currentGame.game_id).count()
        newAchievements = []
        if guess == currentGame.answer:
            currentGame.score = guessCount
            currentGame.end_time = datetime.now()
            currentGame.outcome = "win"
            newAchievements = [a.name for a in check_achievements(user, currentGame)]
        elif guessCount >= len(currentGame.answer)+1:
            currentGame.score = guessCount
            currentGame.end_time = datetime.now()
            currentGame.outcome = "loss"
            newAchievements = [a.name for a in check_achievements(user, currentGame)]
        result = parseResult(guess, currentGame.answer)
        print(guess)
        print(currentGame.answer)
        response = {"result": result, "guessCount": guessCount, "new_achievements": newAchievements}
        if (currentGame.outcome == "loss"):
            response["answer"] = currentGame.answer
        db.session.commit()
        return jsonify(response)
    except:
        print(traceback.format_exc())
        return jsonify({"error": "Some error has occured"}), 400
    


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
    leaderboardRows6 = db.session.execute(text(LEADERBOARD_QUERY6)).fetchall()
    leaderboard6 = [{"firstname6": row[0], "averageScore6": row[1], "averageTime6": row[2], "rank6": row[3]} for row in leaderboardRows6]
    leaderboardRows7 = db.session.execute(text(LEADERBOARD_QUERY7)).fetchall()
    leaderboard7 = [{"firstname7": row[0], "averageScore7": row[1], "averageTime7": row[2], "rank7": row[3]} for row in leaderboardRows7]
    leaderboardRows8 = db.session.execute(text(LEADERBOARD_QUERY8)).fetchall()
    leaderboard8 = [{"firstname8": row[0], "averageScore8": row[1], "averageTime8": row[2], "rank8": row[3]} for row in leaderboardRows8]
    return jsonify(leaderboard, leaderboard6, leaderboard7, leaderboard8)

@app.route('/', defaults = {'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path.startswith('static/') or path.startswith('media/'):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/populate_achievements', methods=['POST'])
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


@app.route('/api/achievement_getter', methods=['GET'])
def achievement_getter():
    authoHeader = request.headers.get('authorization')
    print(authoHeader)
    token = authoHeader.split(" ")[1]
    try:
        decodedJwt = jwt.decode(token, "s{$822Qcg!d*", algorithms=["HS256"])
        user = User.query.filter_by(username=decodedJwt['username']).first()
        achievements = UserAchievement.query.filter_by(user_id=user.user_id).all()
        return jsonify ([achievement.achievement.name for achievement in achievements])
    except:
        print(traceback.format_exc())
        return jsonify({"error": "Invalid token"}), 400
    
@app.route('/api/achievements', methods=['GET'])
def achievements():
    achievements = Achievement.query.all()
    return jsonify([achievement.name for achievement in achievements])

@app.route('/api/createSharedGame', methods=['POST'])
def createSharedGame():
    createGameUuid = str(uuid.uuid4())
    data = request.get_json()
    if not data or 'answer' not in data:
        return jsonify({"error": "Invalid input"}), 400
    answer = data['answer'].lower()
    newSharedGame = SharedGame(
        uuid=createGameUuid,
        answer=answer
    )
    db.session.add(newSharedGame)
    db.session.commit()
    return jsonify({"uuid": createGameUuid})
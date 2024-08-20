from ast import parse
from flask import Flask, request, jsonify, send_from_directory
import random
from models import Game, WordleGuess
from application import app
from db import db
import jwt
from datetime import datetime
import traceback
from sqlalchemy import text
from english_words import get_english_words_set

# Sample word list
WORD_LIST = open("wordle_words.txt").read().splitlines()
LEADERBOARD_QUERY = open("leaderboard.sql").read()
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
    if request.headers.get('game_id'):
        game_id = request.headers.get('game_id')
        currentGame = Game.query.filter_by(game_id=game_id).first()
        if currentGame != None:
            currentGuesses = WordleGuess.query.filter_by(game_id = currentGame.game_id).order_by(WordleGuess.guess_time.asc()).all()
            currentGuesses = [{"guess": guess.guess, "result": parseResult(guess.guess, currentGame.answer)} for guess in currentGuesses]
            return jsonify({ "guesses": currentGuesses, "game_id": currentGame.game_id })
    answer=random.choice(WORD_LIST)
    newGame = Game(
        start_time=datetime.now(),
        answer = answer
    )
    db.session.add(newGame)
    print("Answer: " + newGame.answer)
    db.session.commit()
    return jsonify({ "guesses": [], "game_id": newGame.game_id })

@app.route('/api/guess', methods=['POST'])
def guess():
    data = request.get_json()
    if not data or 'guess' not in data or 'game_id' not in data:
        return jsonify({"error": "Invalid input"}), 400
    guess = data['guess'].lower()
    game_id = data['game_id']
    currentGame = Game.query.filter_by(game_id=game_id).order_by(Game.game_id.desc()).first()
    if guess not in ENGLISH_WORDS:
        return jsonify({"error": "Invalid guess"}), 400
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
    elif guessCount >= len(currentGame.answer)+1:
        currentGame.score = guessCount
        currentGame.end_time = datetime.now()
        currentGame.outcome = "loss"
    result = parseResult(guess, currentGame.answer)
    print(guess)
    print(currentGame.answer)
    response = {"result": result, "guessCount": guessCount}
    if (currentGame.outcome == "loss"):
        response["answer"] = currentGame.answer
    db.session.commit()
    return jsonify(response)

@app.route('/', defaults = {'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path.startswith('static/') or path.startswith('media/'):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

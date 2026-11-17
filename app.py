from flask import Flask, render_template, request, jsonify, session
from wonderwords import RandomWord
import random

app = Flask(__name__)
app.secret_key = "wordle123"

r = RandomWord()
words = [word.upper() for word in r.filter(word_min_length=5, word_max_length=5)]

def new_game():
    session["answer"] = random.choice(words)
    session["attempts"] = 0
    session["game_over"] = False

@app.route("/")
def home():
    new_game()
    return render_template("index.html")

@app.route("/guess", methods=["POST"])
def check_word():
    guess = request.json["guess"].upper()
    answer = session["answer"]

    if session["game_over"]:
        return jsonify(message="Game is over!")

    if guess not in words:
        return jsonify(message="Invalid word!")

    result = ["gray", "gray", "gray", "gray", "gray"]
    remaining = list(answer)

    for i in range(5):
        if guess[i] == answer[i]:
            result[i] = "green"
            remaining[i] = ""

    for i in range(5):
        if guess[i] in remaining and result[i] != "green":
            result[i] = "yellow"
            remaining[remaining.index(guess[i])] = ""

    session["attempts"] += 1

    won = guess == answer

    if won or session["attempts"] == 6:
        session["game_over"] = True

    return jsonify(
        result=result,
        won=won,
        game_over=session["game_over"],
        answer=answer if session["game_over"] else ""
    )

@app.route("/restart", methods=["POST"])
def restart():
    new_game()
    return jsonify(message="New game!")

if __name__ == "__main__":
    app.run(debug=True)

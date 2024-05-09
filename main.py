from flask import Flask, request, jsonify, render_template
import json
import uuid
import random
import os

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)

# const for json file about created jokes
JOKES_FILE_PATH = 'jokesFile.json'

#load jokes from the user-created jokes json
def load_jokes():
    if os.path.exists(JOKES_FILE_PATH):
        with open(JOKES_FILE_PATH, 'r') as f:
            jokes = json.load(f)
    else:
        jokes = []
    return jokes


# Save jokes to user-created jokes JSON file
def save_jokes(jokes):
    with open(JOKES_FILE_PATH, 'w') as f:
        json.dump(jokes, f, indent=5)

# routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loadJokes', methods=['GET'])
def get_jokes():
    jokes = load_jokes()
    return jsonify(jokes)

@app.route('/deleteJoke', methods=['POST'])
def delete_joke():
    joke_id = request.get_data().decode('utf-8')
    jokes = load_jokes()
    jokes = [joke for joke in jokes if joke['jokeID'] != joke_id]
    save_jokes(jokes)
    return jsonify({'message': 'Joke deleted successfully'})

@app.route('/submitJoke', methods=["PUT"])
def submit_joke():
    jokes = request.get_json()
    joke_id = str(uuid.uuid4())
    joke_question = jokes.get("jokeQuestionVar")
    joke_punchline = jokes.get("jokePunchlineVar")
    jokes = load_jokes()
    jokes.append({
        'jokeID': joke_id,
        'jokeQuestion': joke_question,
        'jokePunchline': joke_punchline
    })
    save_jokes(jokes)
    return jsonify({'message': 'Joke submitted successfully'})

@app.route('/generateJoke', methods=["GET"])
def generate_joke():
    with open('jokeDatabase.json', 'r') as k:
        jokesD = json.loads(k.read())
    random_joke = random.choice(jokesD)
    return jsonify(random_joke)

if __name__ == '__main__':
    if not os.path.exists(JOKES_FILE_PATH):
        with open(JOKES_FILE_PATH, 'w') as f:
            f.write('[]')

    app.run(debug=True)


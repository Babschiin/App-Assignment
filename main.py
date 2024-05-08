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
JOKES_FILE_PATH = 'jokesFile.json'

def load_jokes():
    if os.path.exists(JOKES_FILE_PATH):
        with open(JOKES_FILE_PATH, 'r') as f:
            jokes = json.load(f)
    else:
        jokes = []
    return jokes


# Save jokes to JSON file
def save_jokes(jokes):
    with open(JOKES_FILE_PATH, 'w') as f:
        json.dump(jokes, f, indent=5)

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


# #To generate output from the template file
# @app.route('/')
# def index():
#     return render_template('index.html')

# #To read jokes from the jokesFile JSON file
# @app.route('/loadJokes', methods = ['GET'])
# def getJokes():
#     with open('jokesFile.json', 'r') as f:
#         jokes = json.loads(f.read())
#     return jsonify(jokes)

# #The delete button 
# @app.route('/deleteJoke', methods = ['POST'])
# def deleteJoke():
#     jokeID = request.get_data()
#     with open('jokesFile.json', 'r') as f:
#         jokes = json.load(f)
#     jokes = [joke for joke in jokes if joke['jokeID'] != bytes.decode(jokeID)]
#     with open('jokesFile.json', 'w') as f:
#         json.dump(jokes, f, indent=5)

# #Send joke to JSON with the submit button from the input text
# @app.route('/submitJoke', methods = ["PUT"])
# def submitJoke():
#     jokes = request.get_json()
#     jokeID = str(uuid.uuid4())
#     jokeQuestion = jokes.get("jokeQuestionVar")
#     jokePunchline = jokes.get("jokePunchlineVar")
#     with open('jokesFile.json', 'r') as f:
#         jokes = json.load(f)
#     jokes.append({
#         'jokeID' : jokeID,
#         'jokeQuestion' : jokeQuestion,
#         'jokePunchline' : jokePunchline
#         })
#     with open('jokesFile.json', 'w') as f:
#         json.dump(jokes, f, indent=5)

# #For reading the jokeDatabase JSON file
# @app.route('/generateJoke', methods = ["GET"])
# def generateJoke():
#     with open('jokeDatabase.json', 'r') as k:
#         jokesD = json.loads(k.read())
#     randomJoke = random.choice(jokesD)
#     return jsonify(randomJoke)

# if __name__ == '__main__':
#     app.run(debug=True)
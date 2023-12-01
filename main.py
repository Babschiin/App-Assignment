from flask import Flask, request, jsonify, render_template
import json
import uuid
import random

app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)
#To generate output from the template file
@app.route('/')
def index():
    return render_template('index.html')

#To read jokes from the jokesFile JSON file
@app.route('/loadJokes', methods = ['GET'])
def getJokes():
    with open('jokesFile.json', 'r') as f:
        jokes = json.loads(f.read())
    return jsonify(jokes)

#The delete button 
@app.route('/deleteJoke', methods = ['POST'])
def deleteJoke():
    jokeID = request.get_data()
    with open('jokesFile.json', 'r') as f:
        jokes = json.load(f)
    jokes = [joke for joke in jokes if joke['jokeID'] != bytes.decode(jokeID)]
    with open('jokesFile.json', 'w') as f:
        json.dump(jokes, f, indent=5)

#Send joke to JSON with the submit button from the input text
@app.route('/submitJoke', methods = ["PUT"])
def submitJoke():
    jokes = request.get_json()
    jokeID = str(uuid.uuid4())
    jokeQuestion = jokes.get("jokeQuestionVar")
    jokePunchline = jokes.get("jokePunchlineVar")
    with open('jokesFile.json', 'r') as f:
        jokes = json.load(f)
    jokes.append({
        'jokeID' : jokeID,
        'jokeQuestion' : jokeQuestion,
        'jokePunchline' : jokePunchline
        })
    with open('jokesFile.json', 'w') as f:
        json.dump(jokes, f, indent=5)

#For reading the jokeDatabase JSON file
@app.route('/generateJoke', methods = ["GET"])
def generateJoke():
    with open('jokeDatabase.json', 'r') as k:
        jokesD = json.loads(k.read())
    randomJoke = random.choice(jokesD)
    return jsonify(randomJoke)

if __name__ == '__main__':
    app.run(debug=True)
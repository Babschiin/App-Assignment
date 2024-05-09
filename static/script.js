// Loads the jokes on when run
window.onload = function() {
    loadJokes();
  }


// Opens modal when user clicks 'New Joke' button
function openNewJokeModal() {
    document.getElementById("newModal").style.display = 'block';
}

// Opens modal when user clicks 'Generate random joke' button
function openGenerateJokeModal() {
    document.getElementById("generateModal").style.display = 'block';
}

// When the user clicks on the x button, closes modal for the New joke modal box
function closeButton() {
    document.getElementById("newModal").style.display = 'none';
}
// When the user clicks on the x button, closes modal for the Generate random joke box 
function closeButton2() {
    document.getElementById("generateModal").style.display = 'none';
}

// Changes between the joke question and the joke's punchline
function revealJoke(jokeID, jokeSetup, jokePunchline) {
    let jokeElement = document.getElementById(jokeID);
    if (jokeElement.innerHTML === jokeSetup) {
      jokeElement.innerHTML = jokePunchline;
      jokeElement.nextElementSibling.textContent = 'Hide Punchline';
    } else {
      jokeElement.innerHTML = jokeSetup;
      jokeElement.nextElementSibling.textContent = 'Joke Reveal';
    }
  }

// For the New Joke form and submit button
function submitJokeButton() {
    closeButton();
    jokeQuestionVar = document.getElementById("inputBoxQ").value;
    jokePunchlineVar = document.getElementById("inputBoxP").value;
    if (jokeQuestionVar == "" || jokePunchlineVar == "") {
      alert("Please enter both a Question and a Punchline")
      return;
    }
    jokeDataArray = {jokeQuestionVar, jokePunchlineVar}
    var xmlhttprequest = new XMLHttpRequest();
    xmlhttprequest.open("PUT", "/submitJoke");
    xmlhttprequest.setRequestHeader("Content-Type", "application/json");
    xmlhttprequest.send(JSON.stringify(jokeDataArray));
    xmlhttprequest.onload = function () {
      if (xmlhttprequest.status === 200) {
        setTimeout(() => {
          loadJokes();
        }, 400);
      }else {
      console.error("Failed to submit joke")
    }
  };
}

// Sends a request for the delete joke
function deleteJoke(jokeID) {
  randomJokes = randomJokes.filter(joke => joke.jokeID !== jokeID);
  var xmlhttprequest = new XMLHttpRequest();
  xmlhttprequest.open("POST", "/deleteJoke");
  xmlhttprequest.setRequestHeader("Content-Type", "application/json");
  xmlhttprequest.send(jokeID)
  setTimeout(() => { document.location.reload(); }, 400);
}

let randomJokes = []

// Function for adding a new joke entry using New joke to the jokesFile
function loadJokes() {
    fetch("/loadJokes")
    .then(function(response){
        return response.json();
    })
    .then(function(jokes){
        let htmlOutput = document.querySelector("#data-output");
        let jokeList = "";
        for(let joke of jokes){
            jokeList += `
                <li>
                    <div id="jokeList">
                    <p id="${joke.jokeID}">${joke.jokeQuestion}</p>
                    <button type="button" class="button" onclick="revealJoke('${joke.jokeID}', '${joke.jokeQuestion}', '${joke.jokePunchline}')">Joke Reveal</button>
                    <button type="button" class="button" onclick="deleteJoke('${joke.jokeID}')">Joke Delete</button>
                  </div>
                </li>
            `;
        }
        htmlOutput.innerHTML = jokeList;
    });

    fetch("/generatejoke")
    .then(function(response) {
      return response.json();
    })
    .then(function(randomJoke) {
      randomJoke.push(randomJoke);
      displayRandomJokes();
    });
}

// Function for adding random joke entries using the jokeDatabase
// This is the function (most likely causing the issues with the deletion of all items when delete is clicked)
function getNewJoke() {
    fetch("/generateJoke")
      .then(function (response) {
        return response.json();
      })
      .then(function (randomJoke) {
        let jokeList = document.querySelector("#data-output");
        let newJokeItem = document.createElement("li");
        newJokeItem.innerHTML = `
          <div id="jokeList">
            <p id="${randomJoke.jokeID}">${randomJoke.jokeQuestion}</p>
            <button type="button" class="button" onclick="revealJoke('${randomJoke.jokeID}', '${randomJoke.jokeQuestion}', '${randomJoke.jokePunchline}')">Joke Reveal</button>
            <button type="button" class="button" onclick="deleteJoke('${randomJoke.jokeID}')">Joke Delete</button>
          </div>
        `;
        jokeList.appendChild(newJokeItem);
      });
  }
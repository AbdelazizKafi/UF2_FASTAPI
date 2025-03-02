// Faig referencia als elements del document html i dono noms a les funcions que utilitzaré en aquest document
const userGuessInput = document.getElementById('userGuess');
const togglePassword = document.getElementById('togglePassword');
const startGameButton = document.getElementById('startGameButton');
const wordDisplay = document.getElementById('wordDisplay');
const keyboard = document.getElementById('keyboard');
const currentScore = document.getElementById('currentScore');
const totalGames = document.getElementById('totalGames');
const gamesWon = document.getElementById('gamesWon');
const bestGame = document.getElementById('bestGame');

// Aquestes son les diferents variables del joc que s'aniran implementant al llarg del document
let secretWord = '';
let displayedWord = [];
let attemptsLeft = 10;
let score = 0;
let gamesPlayed = 0;
let wonGames = 0;
let bestScore = 0;

// Funció per comptar el numero d'acerts consecutius
let consecutiveCorrectGuesses = 0;
// Alterno la visibilitat de la contrasenya, en el primer cas es mostra i en el segon s'oculta

togglePassword.addEventListener('click', () => {

  if (userGuessInput.type === 'password') {
    userGuessInput.type = 'text'; } 

    else {
userGuessInput.type = 'password';
 }
});

// Inicio el joc i s'obté la paraula secreta que s'ha introduït prèviament
function startGame() {
secretWord = userGuessInput.value.trim().toUpperCase();

// Es valida que s'ha introduït algún contingut a l'input
if (!secretWord) {

alert('Has d’afegir una paraula per poder començar a jugar');
return;
}

// Es valida que no hi hagin números
if (/\d/.test(secretWord)) {

 alert('La paraula no pot contenir números');
 return;

 }
 // Es valida que la paruala tingui que ser superior a 3 caràcters, sinó és mostra una alerta
 if (secretWord.length < 4) {
 alert('La paraula ha de contenir més de 3 caràcters');
 return;

 }

// Inicio l'array i les variables del joc, es es compta el numero de lletres de la parula secreta i en el seu lloc es posen barres baixes _
displayedWord = Array(secretWord.length).fill('_');

attemptsLeft = 10;

// Es reinicia el comptador de acerts seguits
consecutiveCorrectGuesses = 0;
updateWordDisplay();

// Genero el teclat
 generateKeyboard();

startGameButton.disabled = true;
userGuessInput.disabled = true;

fetch('http://localhost:3001/set-secret-word', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ secretWord: secretWord }),
});

}

function updateWordDisplay() {

wordDisplay.textContent = displayedWord.join(' ');
}

// Funció per generar el teclat
function generateKeyboard() {

while (keyboard.firstChild) {

keyboard.removeChild(keyboard.firstChild);

 }

 // Creo els botos de les lletres, cadascuna tinda la seva propia casella i cadascuna serà un botó diferent
 const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
for (const letter of letters) {
 const button = document.createElement('button');
 button.textContent = letter;
 button.addEventListener('click', () => guessLetter(letter, button));

 keyboard.appendChild(button);

 }

}

// Desactivo el botó a l'iniciar la partida i la primera lletra correcta té un valor de 1 punt
function guessLetter(letter, button) {
  button.disabled = true;
  let correct = false;
  let pointsThisRound = 1;
  let occurrences = 0;

for (let i = 0; i < secretWord.length; i++) {
  if (secretWord[i] === letter) {
    displayedWord[i] = letter;
    correct = true;
    occurrences++;
   }
 }

if (correct) {

 // Si la lletra ha sigut encertada, s'incrementa el comptador d'encerts consecutius
 consecutiveCorrectGuesses++;
 pointsThisRound *= occurrences;
 pointsThisRound *= consecutiveCorrectGuesses;

     // Sumo els punts
    score += pointsThisRound;

} else {

// Si no s'acerta, restar un punt pero no pot arribar a ser negatiu
score = Math.max(0, score - 1);
consecutiveCorrectGuesses = 0;

fetch('http://localhost:3001/error-count', {
method: 'POST',
headers: {

 'Content-Type': 'application/json',
},

})
 .then(response => response.json())
.then(data => {

  const limitedErrorCount = Math.min(data.errorCount, 10);
  updateHangmanImage(limitedErrorCount);
 });
 attemptsLeft--;

 if (attemptsLeft === 0) {
checkLoss();
}

 }
 updateWordDisplay();
updateStats();

 if (correct) {
 checkWin();
 }
fetch('http://localhost:3001/error-count', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ letter: letter }),
})
  .then(response => response.json())
  .then(data => {
    const limitedErrorCount = Math.min(data.errorCount, 10);
    updateHangmanImage(limitedErrorCount);
  });
}
// Comprobo si el jugador ha guanyat
function checkWin() {

 if (!displayedWord.includes('_')) {
 gamesPlayed++;
 wonGames++;
 bestScore = Math.max(bestScore, score);
 updateStats();
 alert('Has guanyat!');
 resetGame();

  }
}

// Comprob si el jugador ha perdut
function checkLoss() {
gamesPlayed++;
updateStats();
alert(`Has perdut! La paraula era: ${secretWord}`);
resetGame();

}

// Actualitzo les estadístiques al acabar la partida
function updateStats() {
currentScore.textContent = score;
totalGames.textContent = gamesPlayed;
gamesWon.textContent = wonGames;
bestGame.textContent = `${new Date().toLocaleDateString()} - ${bestScore} punts`;

}

// Es reinicia el joc i totes les dades i les imatges
function resetGame() {
startGameButton.disabled = false;
userGuessInput.disabled = false;
userGuessInput.value = '';
displayedWord = [];
wordDisplay.textContent = 'Començar partida';
attemptsLeft = 10;

  // Es reinicia el número d'errors al reiniciar la partida
   errorCount = 0;

 updateHangmanImage(errorCount);

 while (keyboard.firstChild) {
 keyboard.removeChild(keyboard.firstChild);
   }
 }

document.addEventListener('DOMContentLoaded', () => {

fetch('http://localhost:3001/start-button')
 .then(response => response.text())
 .then(buttonHTML => {
document.getElementById('start-button-container').innerHTML = buttonHTML;
document.getElementById('startGameButton').addEventListener('click', startGame);
 });

fetch('http://localhost:3001/start-text')
.then(response => response.text())
 .then(text => {
document.getElementById('wordDisplay').textContent = text;
 });

 });

// Funció per actualitzar les imatges cada vegada que es falla
function updateHangmanImage(errorCount) {

 const hangmanImageContainer = document.getElementById('hangmanImageContainer');
 hangmanImageContainer.innerHTML = '';
 const hangmanImage = document.createElement('img');

 hangmanImage.src = `img/img_${errorCount}.jpg`;
 hangmanImage.alt = 'Ahorcado';
 hangmanImage.style.maxWidth = '150px';
 hangmanImage.style.marginBottom = '10px';
 hangmanImageContainer.appendChild(hangmanImage);
 }

if (correct) {

 } else {
attemptsLeft--;
 
// Actualitza l'imatge al fallar
 updateHangmanImage(); 
 if (attemptsLeft === 0) {
 checkLoss();
 }
}

 function resetGame() {

 updateHangmanImage();
 }
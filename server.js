const express = require('express');
const cors = require('cors');
const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

let errorCount = 0;
let secretWord = ''; 

//Endpoint botó de començar partida
app.get('/start-button', (req, res) => {
  res.send(`
    <button id="startGameButton" style="
      background-color: rgb(135, 244, 68);
      border: 2px solid rgb(0, 0, 0);
      padding: 10px 20px;
      font-size: 16px;
      border-radius: 5px;
      cursor: pointer;
    ">Començar partida</button>
  `);
});

//Endpoint text començar partida
app.get('/start-text', (req, res) => {
  res.send('Començar partida');
});

// Endpoint per canviar l'imatge al fallar
app.post('/error-count', (req, res) => {
  const selectedLetter = req.body.letter;
  if (secretWord && !secretWord.includes(selectedLetter)) {
    errorCount++;
  }
  res.json({ errorCount });
});

// Endpoint lletres abecedari
app.get('/keyboard', (req, res) => {
  const letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
  let keyboardHTML = '';
  for (const letter of letters) {
    keyboardHTML += `<button class="letter-button" data-letter="${letter}">${letter}</button>`;
  }
  res.send(keyboardHTML);
});

app.post('/set-secret-word', (req, res) => {
  secretWord = req.body.secretWord.toUpperCase();
  errorCount = 0;
  res.send('Palabra secreta establecida');
});

app.listen(port, () => {
  console.log(`Servidor escuchando en el puerto ${port}`);
});
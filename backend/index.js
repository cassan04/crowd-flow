const express = require('express');
const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.json());

app.get('/health', (req, res) => {
  res.status(200).send('Backend OK');
});

app.listen(PORT, () => {
  console.log(`Backend escuchando en puerto ${PORT}`);
});
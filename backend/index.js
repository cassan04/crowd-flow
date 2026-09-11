import app from './src/app.js';
import runConsumer from './src/consumers/kafkaConsumer.js';

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Backend escuchando en puerto ${PORT}`);
});

runConsumer().catch((error) => {
  console.error('Error iniciando el consumidor de Kafka:', error);
});
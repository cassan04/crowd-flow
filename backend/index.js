import app from './src/app.js';
import runConsumer from './src/consumers/kafkaConsumer.js';

const PORT = process.env.API_PORT || 5000;

app.listen(PORT, () => {
  console.log(`Backend listening in port ${PORT}`);
});

runConsumer().catch((error) => {
  console.error('Error initializing Kafka consumer:', error);
});
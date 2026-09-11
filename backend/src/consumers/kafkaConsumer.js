import { Kafka } from 'kafkajs';
import processDetectedMetrics from '../services/metricsService.js';

export let lastData = {
  id: null,
  timestamp: null,
  camera_id: null,
  total_people: 0
}

const kafkaClient = new Kafka({
  clientId: 'crow-backend',
  brokers: [process.env.KAFKA_BROKER || 'kafka:9092'],
});

const consumer = kafkaClient.consumer({ groupId: 'crow-backend-group' });

const runConsumer = async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: 'afluencia_personas_topic', fromBeginning: false });
  
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      try {
        const rawData = JSON.parse(message.value.toString());
        await processDetectedMetrics(rawData, lastData.total_people); 
        lastData = rawData; // Update lastData with the latest received data
      } catch (error) {
        console.error('Error processing message:', error);
      }
    },
  });
};

export default runConsumer;
 
const {Kafka} = require('kafkajs');
const { processDetectedMetrics } = require('../services/metricsService');

const lastData = {
  id: null,
  timestamp: null,
  camera_id: null,
  total_people: 0
}

const kafka = new Kafka({
  clientId: 'crow-backend',
  brokers: [process.env.KAFKA_BROKER || 'kafka:9092'],
});

const consumer = kafka.consumer({ groupId: 'crow-backend-group' });

export const runConsumer = async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: 'afluencia_personas_topic', fromBeginning: false });
  
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      try {
        const rawData = JSON.parse(message.value.toString());
        await processDetectedMetrics(rawData, lastData.total_people); 
        const lastData = rawData; // Update lastData with the latest received data
      } catch (error) {
        console.error('Error processing message:', error);
      }
    },
  });
};

export const getLastData = () => {
  return lastData;
};    
 
const {Kafka} = require('kafkajs');
const { processDetectedMetrics } = require('../services/metricsService');

const kafka = new Kafka({
  clientId: 'crow-backend',
  brokers: [process.env.KAFKA_BROKER || 'kafka:9092'],
});

const consumer = kafka.consumer({ groupId: 'crow-backend-group' });

const runConsumer = async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: 'afluencia_personas_topic', fromBeginning: false });
  
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      try {
        const rawData = JSON.parse(message.value.toString());
        await processDetectedMetrics(rawData); 
      } catch (error) {
        console.error('Error processing message:', error);
      }
    },
  });
};

module.exports = { runConsumer }; 
     
 
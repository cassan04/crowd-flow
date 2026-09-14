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

const TOPIC = 'afluencia_personas_topic';

// The topic is created by the vision service on its first publish, and the
// backend starts first, so it has to create it here: subscribing to a missing
// topic throws UNKNOWN_TOPIC_OR_PARTITION and the consumer never runs.
const ensureTopicExists = async () => {
  const admin = kafkaClient.admin();
  await admin.connect();
  await admin.createTopics({
    topics: [{ topic: TOPIC, numPartitions: 1, replicationFactor: 1 }],
  });
  await admin.disconnect();
};

const runConsumer = async () => {
  await ensureTopicExists();

  await consumer.connect();
  // fromBeginning only applies while the group has no committed offset, so no
  // message is lost if the vision service publishes before this is ready
  await consumer.subscribe({ topic: TOPIC, fromBeginning: true });
  
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
 
const {Kafka} = require('kafkajs');

const kafka = new Kafka({
  clientId: 'crow-backend',
  brokers: [process.env.KAFKA_BROKER || 'kafka:9092'],
});

const consumer = kafka.consumer({ groupId: 'crow-backend-group' });

const runConsumer = async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: 'crow-topic', fromBeginning: false });
  
  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const messageValue = message.value.toString();
      console.log(`Received message: ${messageValue} from topic: ${topic}, partition: ${partition}`);
      // Here you can add your logic to process the message
    },
  });
};

module.exports = { runConsumer };
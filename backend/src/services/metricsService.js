//Here we apply validations about the metrics we are received from the kafka consumer
const metricsModel = require('../models/metricsModel');

const processDetectedMetrics = async (metrics) => {
    const { id, timestamp, camera_id, total_people } = metrics;

    if (total_people === undefined || total_people < 0) return; // Ignore invalid metrics

   return await metricsModel.saveMetrics(id, timestamp, camera_id, total_people);
};

module.exports = {
    processDetectedMetrics
};
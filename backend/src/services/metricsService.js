//Here we apply validations about the metrics we are received from the kafka consumer
const metricsModel = require('../models/metricsModel');

/**
 * Processes detected metrics and saves them to the database or discards them based on certain conditions.
 * @param {Object} metrics - The metrics object received from the kafka consumer
 * @param {number} lastTotalPeople - The last recorded total people count
 * @returns {Promise<void>}
 */
const processDetectedMetrics = async (metrics, lastTotalPeople) => {
    const { id, timestamp, camera_id, total_people } = metrics;

    if (total_people === undefined || total_people < 0) return; // Ignore invalid metrics
    if (total_people === lastTotalPeople) return; // Ignore if the total_people count hasn't changed
   
    return await metricsModel.saveMetrics(id, timestamp, camera_id, total_people);
};

export default processDetectedMetrics;
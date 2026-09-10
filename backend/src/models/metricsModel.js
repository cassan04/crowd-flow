//The connection with the database is made here, and the metrics are stored in the database.

const pool = require('../config/db');

const saveMetrics = async (id, timestamp, camera_id, total_people) => {
    const query = `
        INSERT INTO occupancy_metrics (id, timestamp, camera_id, total_people)
        VALUES ($1, $2, $3, $4)
    `;
    const values = [id, timestamp, camera_id, total_people];

    try {
        await pool.query(query, values);
        console.log('Metrics saved successfully');
    } catch (error) {
        console.error('Error saving metrics:', error);
    }
};

module.exports = {
    saveMetrics
};
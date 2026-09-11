import lastData from '../consumers/kafkaConsumer.js';

export const getMetrics = (req, res) => {
    try {
        res.status(200).json({
            status: 'ok',
            lastData: lastData
        });
    } catch (error) {
        res.status(500).json({
            status: 'error',
            message: error.message
        });
    }
}
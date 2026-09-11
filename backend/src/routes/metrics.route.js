import express from 'express';
import { getMetrics } from '../controllers/metricsController.js';
const metricsRouter = express.Router();

metricsRouter.get('/', getMetrics); // Endpoint to get metrics LastData

export default metricsRouter;
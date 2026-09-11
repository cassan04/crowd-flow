import express from 'express';
import cors from 'cors';
import helmet from 'helmet'; 
import { express as useragent } from 'express-useragent';

import healthRoutes from './routes/health.routes.js';

import corsconfig from './config/cors.config.js';

const API_VERSION = process.env.API_VERSION || 'v1';
const app = express();

app.set('trust proxy', true);
app.use(express.json({limit: '10kb' , strict: true}));
app.use(express.urlencoded({ extended: true, limit: '10kb' }));
app.use(helmet());
app.use(cors(corsconfig));
app.use(useragent());

app.use(`/${API_VERSION}/health`, healthRoutes);
app.use(`/${API_VERSION}/metrics`, metricsRoutes);

export default app;
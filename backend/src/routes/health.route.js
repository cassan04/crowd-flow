import express from 'express'; 
import getStatus from '../controllers/healthController.js';

const healthRouter = express.Router();

healthRouter.get('/', getStatus);

export default healthRouter;
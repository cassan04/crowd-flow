const express = require('express');
const router = express.Router();
const { getStatus } = require('../controllers/healthController');

router.get('/health', getStatus);

module.exports = router;
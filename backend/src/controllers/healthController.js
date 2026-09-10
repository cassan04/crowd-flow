const pool = require('../config/db')

const getStatus = async (req, res) => {
    try {
        const dbResponse = await pool.query('SELECT NOW()')
        res.status(200).json({
            status: 'ok',
            dbTime: dbResponse.rows[0].now
        })
    } catch (error) {
        res.status(500).json({
            status: 'error',
            message: error.message
        })
    }
}

module.exports = {
    getStatus
}
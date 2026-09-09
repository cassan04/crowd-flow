const {Pool} = require('pg')

const pool = new Pool({
    host: process.env.DB_HOST || 'database',
    port: process.env.DB_PORT || 5432,
    database: process.env.DB_NAME || 'afluencia_db',
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || 'examplepassword'
})

pool.on('connect', () => {
    console.log('Connected to the database')
})

pool.on('error', (err) => {
    console.error('Error connecting to the database', err)
})

module.exports = pool
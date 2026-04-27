const oracledb = require('oracledb');

// Thin mode — no Oracle Instant Client needed (same as python-oracledb default)

async function getConnection() {
    return oracledb.getConnection({
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        connectString: process.env.DB_DSN,
        configDir: '/opt/oracle',
        walletLocation: '/opt/oracle',
        walletPassword: process.env.DB_PASSWORD
    });
}

module.exports = { getConnection };

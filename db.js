const oracledb = require('oracledb');

oracledb.initOracleClient({ configDir: '/opt/oracle' });

async function getConnection() {
    return oracledb.getConnection({
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD,
        connectString: process.env.DB_DSN,
        walletLocation: '/opt/oracle',
        walletPassword: process.env.DB_PASSWORD
    });
}

module.exports = { getConnection };

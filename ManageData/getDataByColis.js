const { pool } = require('../app');

module.exports = async function (req, res) {
    const dataColis = req.params.colis;

    try {
        // Get a connection from the pool
        const connection = await pool.getConnection();
        const getOneUser = `SELECT * FROM data WHERE colis = ?`;
        const [colis] = await connection.execute(getOneUser, [dataColis]);
        connection.release(); // Release the connection back to the pool

        if (colis.length === 0) {
            return res.status(404).json({
                success: false,
                message: 'colis not found',
            });
        }

        return res.status(200).json({
            success: true,
            message: 'colis retrieved successfully',
            colis: colis[0], // Return the user data
        });
    } catch (err) {
        console.error("Error getting colis:", err);
        res.status(500).json({
            success: false,
            message: err.message,
        });
    }
};
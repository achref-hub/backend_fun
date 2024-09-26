const { pool } = require('../app');

module.exports = async function (req, res) {
    // Retrieve user info from the JWT token (set in req.user by the verifyToken middleware)
    const userId = req.user.id;

    try {
        // Get a connection from the pool
        const connection = await pool.getConnection();
        const getOneUser = `SELECT * FROM user WHERE id = ?`;
        const [user] = await connection.execute(getOneUser, [userId]);
        connection.release(); // Release the connection back to the pool

        if (user.length === 0) {
            return res.status(404).json({
                success: false,
                message: 'User not found',
            });
        }

        return res.status(200).json({
            success: true,
            message: 'User retrieved successfully',
            user: user[0], // Return the user data
        });
    } catch (err) {
        console.error("Error getting user:", err);
        res.status(500).json({
            success: false,
            message: err.message,
        });
    }
};

const {pool} = require('../app');

module.exports = async function (req, res){
    const userId = req.params.id;

    if (!userId) {
        return res.status(400).json({
            success: false,
            message: 'User ID is required'
        });
    }

    try{
         // Get a connection from the pool
         const connection = await pool.getConnection();
         const getOneUser = `SELECT * FROM user WHERE id = ?`
         const[user] = await connection.execute(getOneUser, [userId]);
         // Release the connection back to the pool
         connection.release();

         if (user.length === 0) {
            return res.status(404).json({
                success: false,
                message: 'User not found'
            });
        }
         return res.status(200).json({
            success: true,
            message: 'user retrieved successfully',
            user: user[0] 
        });
    }catch(err){
        console.error("Error getting user:", err);
        res.status(500).json({
            success :false,
            message :err.message
        })
    }
};
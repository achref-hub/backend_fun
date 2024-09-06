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
         const deleteUser = `DELETE FROM user WHERE id = ?`
         const[users] = await connection.execute(deleteUser, [userId]);
         // Release the connection back to the pool
         connection.release();
         return res.status(200).json({
            success: true,
            message: 'user deleted successfully',
            user: users[0] 
        });
    }catch(err){
        console.error("Error deleting user:", err);
        res.status(500).json({
            success :false,
            message :err.message
        })
    }
};
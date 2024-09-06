const {pool} = require('../app');

module.exports = async function (req, res){
    try{
         // Get a connection from the pool
         const connection = await pool.getConnection();
         const getAllUsers = `SELECT * FROM user`
         const[users] = await connection.execute(getAllUsers, null);
         // Release the connection back to the pool
         connection.release();
         return res.status(200).json({
            success: true,
            message: 'All users returned successfully',
            user: users[0] 
        });
    }catch(err){
        console.error("Error getting users:", err);
        res.status(500).json({
            success :false,
            message :err.message
        })
    }
};
const {pool} = require('../app');

module.exports = async function (req, res){
    try{
         // Get a connection from the pool
         const connection = await pool.getConnection();
         const getAllStats = `SELECT * FROM stats_table`
         const[Stats] = await connection.execute(getAllStats, null);
         // Release the connection back to the pool
         connection.release();
         return res.status(200).json({
            success: true,
            message: 'All Stats returned successfully',
            Stats: Stats
        });
    }catch(err){
        console.error("Error getting Stats:", err);
        res.status(500).json({
            success :false,
            message :err.message
        })
    }
};
const {pool} = require('../app');

module.exports = async function (req, res){
    try{
         // Get a connection from the pool
         const connection = await pool.getConnection();
         const getAllData = `SELECT * FROM data`
         const[data] = await connection.execute(getAllData, null);
         // Release the connection back to the pool
         connection.release();
         return res.status(200).json({
            success: true,
            message: 'All data returned successfully',
            data: data
        });
    }catch(err){
        console.error("Error getting data:", err);
        res.status(500).json({
            success :false,
            message :err.message
        })
    }
};
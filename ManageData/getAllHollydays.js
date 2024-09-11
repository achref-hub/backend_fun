const {pool} = require('../app');

module.exports = async function (req, res){
    try{
         // Get a connection from the pool
         const connection = await pool.getConnection();
         const getAllHollydays = `SELECT * FROM hollydays_table`
         const[hollydays] = await connection.execute(getAllHollydays, null);
         // Release the connection back to the pool
         connection.release();
         return res.status(200).json({
            success: true,
            message: 'All Hollydays returned successfully',
            hollydays: hollydays
        });
    }catch(err){
        console.error("Error getting Hollydays:", err);
        res.status(500).json({
            success :false,
            message :err.message
        })
    }
};
const {pool} = require('../app');

module.exports = async function (req, res){
    const colis = req.params.colis;
    if (!colis) {
        return res.status(400).json({
            success: false,
            message: 'colis is required'
        });
    }
    try{
         // Get a connection from the pool
         const connection = await pool.getConnection();
         const deleteData = `DELETE FROM data WHERE colis = ?`
         const[data] = await connection.execute(deleteData, [colis]);
         // Release the connection back to the pool
         connection.release();
         return res.status(200).json({
            success: true,
            message: 'data deleted successfully',
            data: data[0] 
        });
    }catch(err){
        console.error("Error deleting data:", err);
        res.status(500).json({
            success :false,
            message :err.message
        })
    }
};
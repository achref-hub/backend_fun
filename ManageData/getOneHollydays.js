const {pool} = require('../app');

module.exports = async function (req, res){
    const hollydayByGouvernorat = req.params.Gouvernorat;

    if (!hollydayByGouvernorat) {
        return res.status(400).json({
            success: false,
            message: 'hollyday is required'
        });
    }

    try{
         // Get a connection from the pool
         const connection = await pool.getConnection();
         const getOneHollyday = `SELECT * FROM hollydays_table WHERE Gouvernorat = ?`
         const[hollyday] = await connection.execute(getOneHollyday, [hollydayByGouvernorat]);
         // Release the connection back to the pool
         connection.release();

         if (hollyday.length === 0) {
            return res.status(404).json({
                success: false,
                message: 'hollyday not found'
            });
        }
         return res.status(200).json({
            success: true,
            message: 'hollyday retrieved successfully',
            hollyday: hollyday[0] 
        });
    }catch(err){
        console.error("Error getting hollyday:", err);
        res.status(500).json({
            success :false,
            message :err.message
        })
    }
};
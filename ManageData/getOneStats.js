const {pool} = require('../app');

module.exports = async function (req, res){
    const statByGouvernorat = req.params.Gouvernorat;

    if (!statByGouvernorat) {
        return res.status(400).json({
            success: false,
            message: 'stat is required'
        });
    }

    try{
         // Get a connection from the pool
         const connection = await pool.getConnection();
         const getOneStat = `SELECT * FROM stats_table WHERE Gouvernorat = ?`
         const[stat] = await connection.execute(getOneStat, [statByGouvernorat]);
         // Release the connection back to the pool
         connection.release();

         if (stat.length === 0) {
            return res.status(404).json({
                success: false,
                message: 'stat not found'
            });
        }
         return res.status(200).json({
            success: true,
            message: 'hollyday retrieved successfully',
            stat: stat[0] 
        });
    }catch(err){
        console.error("Error getting stat:", err);
        res.status(500).json({
            success :false,
            message :err.message
        })
    }
};
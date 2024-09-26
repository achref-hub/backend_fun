const { pool } = require('../app');

module.exports = async function (req, res) {
    const colis = req.params.colis;
    // Destructure request body
    const { 
        nomDestinataire, 
        tel1, 
        tel2 = null,
        genre, 
        Gouvernorat, 
        description, 
        statut, 
        dateCreation, 
        crApresRemise = null
    } = req.body;

    // SQL query
    const sql = `Update data SET colis = ?, nomDestinataire = ?, tel1 = ?, tel2 = ?, genre = ?, Gouvernorat = ?, description = ?, statut = ?, dateCreation = ?, crApresRemise = ? WHERE colis = ?`;

    try {
        // Get a connection from the pool
        const connection = await pool.getConnection();
        
        // Execute the SQL query and pass sanitized values
        const [result] = await connection.execute(sql, [
            colis || null,
            nomDestinataire || null, 
            tel1 || null, 
            tel2,  
            genre || null, 
            Gouvernorat || null, 
            description || null, 
            statut || null, 
            dateCreation || null, 
            crApresRemise || null,
            colis
        ]);

        const getData = `SELECT * FROM data WHERE colis = ?`;
        const [data] = await connection.execute(getData, [colis]);

        // Release the connection
        connection.release();

        // Return success response
        return res.status(200).json({
            success: true,
            message: 'row updated successfully',
            data: data[0],
        });

    } catch (err) {
        console.error("Error updating row:", err);

        // Return error response
        return res.status(500).json({
            success: false,
            message: err.message, 
        });
    }
};

const {pool} = require('../app');
const bcrypt = require('bcrypt');
const { v4: uuidv4 } = require('uuid');

module.exports = async function (req, res){
    const id = uuidv4();
    const { full_name, email, password } = req.body;
    const sql = `INSERT INTO user (id, full_name, email, password ) VALUES (?, ?, ?, ?)`
    try{
        const saltRounds = 10; 
        const hashedPassword = await bcrypt.hash(password, saltRounds);
        console.log("hashedPassword",hashedPassword);
         // Get a connection from the pool
         const connection = await pool.getConnection();
         const [result] = await connection.execute(sql, [id, full_name, email, hashedPassword]);

         const getOneUser = `SELECT * FROM user where id = ?`
         const[user] = await connection.execute(getOneUser, [id]);
         // Release the connection back to the pool
         connection.release();
         return res.status(200).json({
            success: true,
            message: 'User created successfully',
            user: user[0] 
        });
    }catch(err){
        console.error("Error creating user:", err);
        res.status(500).json({
            success :false,
            message :err.message
        })
    }
};
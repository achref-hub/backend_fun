const { pool } = require('../app');
const bcrypt = require('bcrypt');
const { v4: uuidv4 } = require('uuid');
const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET;

module.exports = async function (req, res) {
    const id = uuidv4();
    const { full_name, email, password } = req.body;
    const sql = `INSERT INTO user (id, full_name, email, password) VALUES (?, ?, ?, ?)`;

    try {
      
        const saltRounds = 10;
        const hashedPassword = await bcrypt.hash(password, saltRounds);

        // Get a connection from the pool
        const connection = await pool.getConnection();

        // Check if email already exists
          const checkEmail = `SELECT email FROM user WHERE email = ?`;
          const [rows] = await connection.execute(checkEmail, [email]);
          if (rows.length > 0) {
              return res.status(400).json({
                  success: false,
                  message: 'Email already exists'
              });
          };

        // Insert the user into the database
        await connection.execute(sql, [id, full_name, email, hashedPassword]);

        // Retrieve the user after inserting
        const getOneUser = `SELECT * FROM user WHERE id = ?`;
        const [user] = await connection.execute(getOneUser, [id]);

        // Release the connection back to the pool
        connection.release();

        // Generate JWT Token for the newly created user
        const token = jwt.sign(
            { id: user[0].id, email: user[0].email }, 
            JWT_SECRET, 
            { expiresIn: '24h' } 
        );

        // Return response with user details and JWT token
        return res.status(200).json({
            success: true,
            message: 'User created successfully',
            token, 
            user: {
                id: user[0].id,
                full_name: user[0].full_name,
                email: user[0].email
            }
        });
    } catch (err) {
        console.error("Error creating user:", err);
        return res.status(500).json({
            success: false,
            message: err.message
        });
    }
};

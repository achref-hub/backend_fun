const jwt = require('jsonwebtoken');
const JWT_SECRET = process.env.JWT_SECRET; 

module.exports = function (req, res, next) {
    const token = req.header('Authorization')?.split(' ')[1]; // Extract the token part

    if (!token) {
        return res.status(401).json({ success: false, message: 'Access denied. No token provided.' });
    }

    try {
        const decoded = jwt.verify(token, JWT_SECRET);
        console.log('Decoded:', decoded); // Debug log
        req.user = decoded; // Attach the user payload to the request
        next();
    } catch (err) {
        console.error('Token verification error:', err); // Debug log
        res.status(400).json({ success: false, message: 'Invalid token.' });
    }
};

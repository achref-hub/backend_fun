const jwt = require('jsonwebtoken');
const JWT_SECRET = process.env.JWT_SECRET; 

module.exports = function (req, res, next) {
    const token = req.header('Authorization')?.split(' ')[1]; 

    if (!token) {
        return res.status(401).json({ success: false, message: 'Access denied. No token provided.' });
    }

    try {
        const decoded = jwt.verify(token, JWT_SECRET);
        req.user = decoded; // Attach the user payload to the request
        next();
    } catch (err) {
        res.status(400).json({ success: false, message: 'Invalid token.' });
    }
};

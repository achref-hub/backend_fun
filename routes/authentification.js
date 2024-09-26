const express = require("express");
const router = express.Router();

const signIn = require('../authentication/signIn');
const signUp = require('../authentication/signUp');
const auth = require('../authentication/authMiddleware');

router.post("/sign-in", signIn);
router.post("/sign-up", signUp);

// Protected route to get the logged-in user's details
router.get("/profile", auth, (req, res) => {
    res.json({ success: true, message: "Authenticated user", user: req.user });
});
module.exports = router;
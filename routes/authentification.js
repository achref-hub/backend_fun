const express = require("express");
const router = express.Router();

const signIn = require('../authentication/signIn');
const signUp = require('../authentication/signUp');
const auth = require('../authentication/authMiddleware');

router.post("/sign-in", signIn);
router.post("/sign-up", signUp);

// Protected route example (must be authenticated)
router.get("/protected", auth, (req, res) => {
    res.json({ success: true, message: "You have access to this protected route", user: req.user });
});
module.exports = router;
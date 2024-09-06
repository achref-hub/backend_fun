const express = require("express");
const router = express.Router();

const signIn = require('../authentication/signIn');

router.post("/sign-in", signIn);


module.exports = router;
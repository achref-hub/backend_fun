const express = require("express");
const router = express.Router();

const addNewUser = require('../User/create');
const getAllUsers = require('../User/getAll');
const getUserById = require('../User/getOne');
const deleteUserById = require('../User/delete');
const auth = require('../authentication/authMiddleware');

router.post("/add", addNewUser);
router.get("/getAll", getAllUsers);
router.delete('/:id', deleteUserById);
router.get("/me", auth, getUserById); 



module.exports = router;

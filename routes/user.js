const express = require("express");
const router = express.Router();

const addNewUser = require('../User/create');
const getAllUsers = require('../User/getAll');
const getUserById = require('../User/getOne');
const deleteUserById = require('../User/delete');

router.post("/add", addNewUser);
router.get("/getAll", getAllUsers);
router.get('/:id', getUserById);
router.delete('/:id', deleteUserById);



module.exports = router;

const express = require("express");
const router = express.Router();

const addNewData = require('../ManageData/importCsv.js');

router.post("/addData", addNewData);

module.exports = router;

const express = require("express");
const router = express.Router();

const getAllHollydays = require('../ManageData/getAllHollydays');
const getAllStats = require('../ManageData/getAllStats');
const getOneHollyday = require('../ManageData/getOneHollydays');
const getOneStat = require('../ManageData/getOneStats');

router.get("/getAllHollydays", getAllHollydays);
router.get("/getAllStats", getAllStats);

router.get('/hollyday/:Gouvernorat', getOneHollyday);
router.get('/stat/:Gouvernorat', getOneStat);



module.exports = router;

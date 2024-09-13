const express = require("express");
const router = express.Router();

const getAllHollydays = require('../ManageData/getAllHollydays');
const getAllStats = require('../ManageData/getAllStats');
const getOneHollyday = require('../ManageData/getOneHollydays');
const getOneStat = require('../ManageData/getOneStats');
const createNewData = require('../ManageData/createData');
const getAllData =require('../ManageData/getData');
const deleteData = require('../ManageData/deleteData');

router.get("/getAllHollydays", getAllHollydays);
router.get("/getAllStats", getAllStats);
router.post("/create/newData", createNewData);
router.get('/allData',getAllData );
router.delete('/delete/:colis', deleteData);
router.get('/hollyday/:Gouvernorat', getOneHollyday);
router.get('/stat/:Gouvernorat', getOneStat);



module.exports = router;

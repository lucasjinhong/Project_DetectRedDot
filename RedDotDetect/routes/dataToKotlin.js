var express = require('express');
var path = require('path');
var router = express.Router();
var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({limit: '50mb', extended: true});

var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";

router.get('/first10Record', function(req, res, next){
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var dbo = db.db("DetectRedDot");

        var mysort = { time: -1 };
        var query = {};
        var projection = {_id:0, image:0};

        dbo.collection("RedDot").find(query).project(projection).sort(mysort).limit(10).toArray(function(err, result) {

          if (err) throw err;
          db.close();
          console.log('\nResult sent');
          res.send({result:result});
        });
    });
});

module.exports = router;
var express = require('express');
var path = require('path');
var router = express.Router();
var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({limit: '50mb', extended: true});

var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";
 
router.post('/',urlencodedParser, (req, res, next) => {
    response = 
    {  
        color:req.body.color,  
        value:req.body.value,
        date:req.body.time,
        img:req.body.imgBase64
    };

    res.send(response); 
   
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var dbo = db.db("DetectRedDot");
        var myobj = [{time: new Date(), records:{color:response.color, value:response.value}, image:response.img}];
        dbo.collection("RedDot").insertMany(myobj, function(err, res) {
          if (err) throw err;
          console.log(res, '\n' , {color:response.color, value:response.value}, '\n');
          db.close();
        });
    });
})

router.get('/data', function(req, res, next){
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var dbo = db.db("DetectRedDot");
        var mysort = { time: -1 };
        dbo.collection("RedDot").find({}).sort(mysort).limit(1).toArray(function(err, result) {
          if (err) throw err;
          db.close();
          console.log(result[0]);
          res.send(result[0]);
        });
    });
 });

module.exports = router;

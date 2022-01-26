var express = require('express');
var path = require('path');
var router = express.Router();
var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({ extended: false });

var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";

router.get('/', function(req, res, next) {
    res.send("Hello");
});

router.post('/',urlencodedParser, (req, res, next) => {
    response = req.body
    /*{  
        color:req.body.color,  
        value:req.body.value 
    };*/
    console.log(response);
    
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var dbo = db.db("DetectRedDot");
        var myobj = [{record:response}];
        dbo.collection("RedDot").insertMany(myobj, function(err, res) {
          if (err) throw err;
          console.log(res);
          db.close();
        });
    });
    console.log("data inserted");
    
    res.send(response); 
    
    ///setTimeout(() => res.redirect('/detect'), 5000);
    ///console.log("redirecting");
})

module.exports = router;

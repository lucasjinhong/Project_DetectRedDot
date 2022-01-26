var express = require('express');
var path = require('path');
var router = express.Router();
var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({ extended: false });

var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";

/* GET home page. */
router.get('/', function(req, res, next) {
    res.sendFile(path.join(__dirname, './website/detect.html'));
});

router.post('/answer',urlencodedParser, (req, res, next) => {
    response = {  
        color:req.body.color,  
        value:req.body.value 
    };  
    console.log(response);
    
    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var dbo = db.db("DetectRedDot");
        var myobj = [response];
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

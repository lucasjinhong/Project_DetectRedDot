var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";

MongoClient.connect(url, function(err, db) {
  if (err) throw err;
  var dbo = db.db("DetectRedDot");
  var myobj = [
    {name: 'first', value:5},
    {name: 'second', value:6},
    {name: 'thrid', value:7}
  ];
  dbo.collection("RedDot").insertMany(myobj, function(err, res) {
    if (err) throw err;
    console.log(res);
    db.close();
  });
});
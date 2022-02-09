var express = require('express');  
var app = express();  
app.use(express.static('public')); 
var bodyParser = require('body-parser');
var urlencodedParser = bodyParser.urlencoded({ extended: false }); 
  
app.get('/index.html', function (req, res) {  
   res.sendFile( __dirname + "/" + "index.html" );  
})  

app.post('/index.html/progress',urlencodedParser, (req, res, next) => {  
   response = { 
      records : [ 
         {
            color: req.body.first_name,
            value: req.body.last_name
         }
      ] 
   };  
   console.log(response);  
   res.end(JSON.stringify(response));  
})  
var server = app.listen(8000, function () {  
  
  var host = server.address().address  
  var port = server.address().port  
  console.log("Example app listening at http://%s:%s", host, port)  
  
})  
var express = require('express');
var router = express.Router();

const mqtt = require('mqtt')

const host = '140.124.73.217'
const port = '1883'
const topic = 'NTUT/Find-red'
const clientId = `mqtt_${Math.random().toString(16).slice(3)}`

const connectUrl = `mqtt://${host}:${port}`
const client = mqtt.connect(connectUrl, {
  clientId,
  clean: true,
  connectTimeout: 4000,
  username: '',
  password: '',
  reconnectPeriod: 1000,
})

/*
var MongoClient = require('mongodb').MongoClient;
var url = "mongodb://localhost:27017/";

client.on('connect', () => {
    console.log('\nMQTT Connected')

    client.subscribe([topic], () => {
      console.log(`Subscribe to topic '${topic}'`)
    })
})

client.on('message', (topic, payload) => {

    var imgData = JSON.parse(payload.toString());
    var response = {
        color:imgData.color,
        value:imgData.value
    }
    var imgBase64 = imgData.imgBase64;

    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var dbo = db.db("DetectRedDot");
        var myobj = [{time: new Date(), records:response, image:imgBase64}];
        dbo.collection("RedDot").insertMany(myobj, function(err, res) {
          if (err) throw err;
          console.log('\nData Inserted:', res);
          db.close();
        });
    });
    console.log('\nMQTT Received Message:', response)
})
*/

module.exports = router;
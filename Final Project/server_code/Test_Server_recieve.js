///--------------------------------------------------------------------

var express = require("express");
var app = express();
var bodyParser = require('body-parser');
var errorHandler = require('errorhandler');
var methodOverride = require('method-override');
var hostname = process.env.HOSTNAME || 'localhost';
var port = 8080;

var parkval;

app.use(methodOverride());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static(__dirname + '/public'));
app.use(errorHandler());


app.post("/update_space_counter", function (req, res) {
    const space_counter = req.body.space_counter;
    // Handle the received spaceCounter data as needed
    console.log(`Available parking space: ${space_counter}`);
    
    // Send a response back to the Python script
    res.send("Space counter received successfully.");
});

app.get("/get_space_counter", function (req, res) {
    var ret = {
        space_counter: space_counter
    };
    res.send(JSON.stringify(ret));
});

console.log("Simple static server listening at http://" + hostname + ":" + port);
app.listen(port);
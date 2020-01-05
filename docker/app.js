var express = require("express");
var bodyParser = require("body-parser");
var cors = require("cors");
var app = express();

// initialization
app.listen(8080, () => {
  console.log("Server running on port 8080.");
});
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// POST request that hashes the user input.
app.post("/messages", (req, res, next) => {

});

// GET request that returns the original message.
app.get("/messages/:id", (req, res, next) => {

});
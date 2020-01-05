const express = require("express");
const bodyParser = require("body-parser");
const cors = require("cors");
var app = express();
var message = require("./message");

app.listen(8080, () => {
  console.log("Server running on port 8080.");
});
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// POST request that hashes the user input.
app.post("/messages", (req, res) => {
  const data = req.body;
  const hash = message.hashMessage(JSON.stringify(data));
  const digest = {
    digest: hash
  };
  res.send(digest);
});

// GET request that returns the original message.
app.get("/messages/:hash", (req, res) => {
  const hash = req.params.hash;
  const resp = message.retrieveMessage(hash);
  if (resp == null) {
    const err = {
      err_msg: "Message not found"
    };
    res.status(404).send(err);
  } else {
    res.send(resp);
  }
});

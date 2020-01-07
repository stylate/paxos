const crypto = require("crypto");

var digests = {}; // key: hash, value: exposed message

var hashMessage = msg => {
  var hash = crypto
    .createHash("sha256")
    .update(msg)
    .digest("hex");
  digests[hash] = msg;
  return hash;
};

var retrieveMessage = hash => {
  if (hash in digests) {
    return digests[hash];
  }
  return null;
};

module.exports = {
  hashMessage: hashMessage,
  retrieveMessage: retrieveMessage
};

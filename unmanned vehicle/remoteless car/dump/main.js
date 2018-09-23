var express = require('Express');
var app = express();
var others = require('./other.js');

//both index.js and things.js should be in same directory
app.use('/others', others);

app.listen(5000);

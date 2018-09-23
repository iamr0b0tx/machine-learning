//create server
var express = require('express');
var router = express.Router();

// Read the requested file content from file system
function read(filename){
	var content = "";
	fs.readFile(filename, function (err, data) {
		if(err){
			console.log(err);
			content = "";
			
		}else{
			
			content = data.toString();
			
		}
	});
	return content;
}

router.get('/', function(req, res){
//		res.send(read("index.html"));
		res.send('GET route on things.');

	});
	
router.post('/', function(req, res){
	res.send('POST route on things.');
});

//export this router to use in our index.js
module.exports = router;


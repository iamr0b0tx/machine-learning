<!DOCTYPE html>
<html>

	<head>

		<title>Creating an HTML Element</title>
		
		<style>
			#space{
				width:100%;
				height:100%;
				padding:.5%;
				background-color:#555;
			}
			.full{
				width:100%;
				height:600px;
			}
			.vcar, .car{
				background-color:red;
				width:30px;
				height:15px;
				position:absolute;
				top:0px;
				left:0px;
				transform:rotate(0deg);
				z-index:1;
			}
			.vcar{
				background-color:blue;
				z-index:2;
				border-radius:100%;
				width:5px;
				height:5px;
			}
	  </style>
	  
		<script>
			function read_key(event){}
			
			function set_target(event) {}
		</script>
	</head>

	<body >
		<div id="space" class="full" onclick="set_target(event)">
			<div id="car" class="car">
				
			</div>
			
			<div id="vcar" class="vcar">
				
			</div>
		</div>
		
		<script>
			document.getElementById("space").style.height = screen.availHeight*0.79+"px";
			document.getElementById("space").style.width = screen.availWidth*0.98+"px";
			
			function set_target(event){
				target = "{\"x\":"+event.clientX+", \"y\":"+event.clientY+", \"z\":0}";
				var data = JSON.parse(target);
				id = "vcar"
				//console.log(data["tetha_xy"]);
				
				document.getElementById(id).style.left = parseInt(data["x"]).toString()+"px";
				document.getElementById(id).style.top = parseInt(data["y"]).toString()+"px";
				document.getElementById(id).style.transform = "rotate("+data["tetha_xy"]+"deg)";
				console.log("target = " + target)
				send_req("set_position", target);
			}
			
			function send_req(key, val, id="car"){
				if (window.XMLHttpRequest) {
					// code for IE7+, Firefox, Chrome, Opera, Safari
					xmlhttp = new XMLHttpRequest();
				} else {
					// code for IE6, IE5
					xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
				}
				xmlhttp.onreadystatechange = function() {
					if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
						text = xmlhttp.responseText;
						//console.log(text);
						if(key == "get_position"){
							var data = JSON.parse(text);
							//console.log(data["tetha_xy"]);
							
							document.getElementById(id).style.left = parseInt(data["x"]-15).toString()+"px";
							document.getElementById(id).style.top = parseInt(data["y"]-7.5).toString()+"px";
							document.getElementById(id).style.transform = "rotate("+data["tetha_xy"]+"deg)";
						}
					}
				}
				xmlhttp.open("POST","query.php?"+key+"="+val, true);
				xmlhttp.send();
			}
			
			function update(){
				send_req("get_position", "position.json");
				
				
			}
			setInterval(update, 100);
		</script>
	</body>
</html>
//THIS MODULE IS PURE POETRY BEAUTIFULLY CRAFTED MOTHERFUCKINESS
$(document).ready(function(){
	realtimeToday = true;
	if(realtimeToday==true) {
		options.size = 130;
		options.step = 10;
		xCameraPosition = 65;
		yCameraPosition = 65;
		zCameraPosition = 65;
		radiusCamera = 230;
	}

	//LOAD TODAY STOCKS FOR GOOGLE
	$.get( "realtimestocks/GOOG", function( data ) {
	  //$( ".result" ).html( data );
	  //alert( "Load was performed." );
	  axis = data.split("\n");
	  xAxisR = axis[0].split(",");
	  yAxisR = axis[1].split(",");
	  zAxisR = axis[2].split(",");
	  // alert(xAxisR.length);
	  // if(xAxisR.length==yAxisR.length && yAxisR.length==zAxisR.length){
	  // 	alert("yes");
	  // }
	  // else {
	  // 	alert("no");
	  // }
	  xAxis = new Array();
	  yAxis = new Array();
	  zAxis = new Array();
	  for(i=0; i<xAxisR.length; i++){
	  	xAxis[i] = parseInt(xAxisR[i]);
	  	yAxis[i] = parseInt(yAxisR[i]);
	  	zAxis[i] = parseInt(zAxisR[i]);
	  }
	  // alert(xAxis.length);
	  newLine = new Line(xAxis, yAxis, zAxis);
	  allTheLines.add(newLine.getLine());
	});
	/*------------
	------------------------------------------------------------
	------------------------------------------------------------
	------------------------------------------------------------
	INITIATION CALLS
	------------------------------------------------------------
	------------------------------------------------------------
	------------------------------------------------------------
	*/
	initGraphing();
	animateGraphing();
});
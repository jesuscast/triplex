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
	// $.get( "realtimestock/GOOG", function( data ) {
	//   //$( ".result" ).html( data );
	//   ////alert( "Load was performed." );
	//   axis = data.split("\n");
	//   xAxisR = axis[0].split(",");
	//   yAxisR = axis[1].split(",");
	//   zAxisR = axis[2].split(",");
	//   // //alert(xAxisR.length);
	//   // if(xAxisR.length==yAxisR.length && yAxisR.length==zAxisR.length){
	//   // 	//alert("yes");
	//   // }
	//   // else {
	//   // 	//alert("no");
	//   // }
	//   xAxis = new Array();
	//   yAxis = new Array();
	//   zAxis = new Array();
	//   for(i=0; i<xAxisR.length; i++){
	//   	xAxis[i] = parseInt(xAxisR[i]);
	//   	yAxis[i] = parseInt(yAxisR[i]);
	//   	zAxis[i] = parseInt(zAxisR[i]);
	//   }
	//   // //alert(xAxis.length);
	//   newLine = new Line(xAxis, yAxis, zAxis);
	//   allTheLines.add(newLine.getLine());
	// });


	//LOAD TODAY STOCKS FOR SEVERAL COMPANIES
	$.get( "stocks-xyz/AAPL,GE", function( data ) {
	  initGraphing();
	  animateGraphing();
	  stocks = data.split("^");
	  //alert(stocks.length);
	  newLine = null;
	  var i = 0;
	  while(i<stocks.length){
		//alert(i);
		var thisStock = stocks[i].split("%");
		//prompt("stock #"+i.toString(),thisStock.length);
		var xAxisR = thisStock[0].split(",");
		var yAxisR = thisStock[1].split(",");
		var zAxisR = thisStock[2].split(",");
		//alert("Axis Rx:"+xAxisR.length.toString());
		//prompt("Axis Rx",xAxisR.join(','))
		//alert("Axis Ry:"+yAxisR.length.toString());
		//prompt("Axis Ry",yAxisR.join(','))
		//alert("Axis Rz:"+zAxisR.length.toString());
		//prompt("Axis Rz",zAxisR.join(','))
		var xAxis = new Array();
		var yAxis = new Array();
		var zAxis = new Array();
		for(j=0; j<xAxisR.length; j++){
			xAxis[j] = parseInt(xAxisR[j]);
			yAxis[j] = parseInt(yAxisR[j]);
			zAxis[j] = parseInt(zAxisR[j]);
		}
		//alert("Axis x:"+xAxis.length.toString());
		//alert("Axis y:"+yAxis.length.toString());
		//alert("Axis z:"+zAxis.length.toString());
		var newLine = new Line(xAxis, yAxis, zAxis);
		allTheLines.add(newLine.getLine());
		i+=1;
	  }

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
});
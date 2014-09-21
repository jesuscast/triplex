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

	//LOAD TODAY STOCKS FOR SEVERAL COMPANIES
	
initGraphing();
animateGraphing();
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

function loadStocks(){
	allTheStocksString = allTheStocks.join();
	$.get( "stocks-xyz/"+allTheStocksString, function( data ) {
	  initGraphing();
	  animateGraphing();
	  stocks = data.split("^");
	  newLine = null;
	  var i = 0;
	  while(i<stocks.length){
		var thisStock = stocks[i].split("%");
		var xAxisR = thisStock[0].split(",");
		var yAxisR = thisStock[1].split(",");
		var zAxisR = thisStock[2].split(",");
		var xAxis = new Array();
		var yAxis = new Array();
		var zAxis = new Array();
		for(j=0; j<xAxisR.length; j++){
			xAxis[j] = parseInt(xAxisR[j]);
			yAxis[j] = parseInt(yAxisR[j]);
			zAxis[j] = parseInt(zAxisR[j]);
		}
		var newLine = new Line(xAxis, yAxis, zAxis);
		// newLine.indexStock = currentLineIndex;
		// currentLineIndex += 1;
		//stockIndexes[i] = allTheStocks[i];
		allTheLines.add(newLine.getLine());
		i+=1;
	  }

	});
}
// function deleteStock(indexStock){
// 	for(i=0; i<allTheLines.children.length; i++){
// 		if(stock == indexStock){
// 			allTheLines.remove(allTheLines.children[i]);
// 		}
// 	}
//}

function cleanGraph(){
	for(i = 0; i<allTheLines.children.length; i++){
		allTheLines.children.remove(i);
	}
}	
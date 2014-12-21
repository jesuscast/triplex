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
	allTheStocksNames = allTheStocks.items();
	$.get( "stocks-xyz/"+allTheStocksNames.join()+"?fromDate=1,12,2014&toDate=10,12,2014", function( data ) {
	  //clean the previous array of stocks
	  stocksArray = new Array();
	  initGraphing();
	  animateGraphing();
	  rawData = data.split("-MAXIMUMSEPARATOR-");
	  tempMatrix = rawData[0].split("###");
	  allTheStocksData = [];
	  for(var i = 0; i<tempMatrix.length; i++){
    	matrixTemp = tempMatrix[i].split("^");
		matrixTempI = [];
		for(var j = 0; j<matrixTemp.length; j++){
	    	matrixTempI[matrixTempI.length]= matrixTemp[j].split(",");
		}
		allTheStocksData[allTheStocksData.length]= [allTheStocksNames[i],matrixTempI];
	  }
	  stocks = rawData[1].split("^");
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
		var newLine = new Line(xAxis, yAxis, zAxis, allTheStocksColors.items()[i][1]);
		//add the indexes to a new array element in stocks Array
		//stocksArray[stocksArray.length] = [allTheStocksNames[i],xAxis, yAxis, zAxis];
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

function onDocumentMouseDown(event){
	//event.preventDefault();
	if(pointSelected==true){
		indexSelected = allTheLines.children.indexOf(intersectedObject.object);
		//selectedPointLOL = allTheStocksData[indexSelected];
		selectedPointLOL = allTheStocksData[indexSelected][1][parseInt(allTheStocksData[indexSelected][1].length/130.0*intersectedObject.point.x)];
		$stocksDisplay = $("#stockDisplay");
		$stocksDisplay.find("#date span").text(selectedPointLOL[0]);
		$stocksDisplay.find("#open span").text(selectedPointLOL[1]);
		$stocksDisplay.find("#high span").text(selectedPointLOL[2]);
		$stocksDisplay.find("#low span").text(selectedPointLOL[3]);
		$stocksDisplay.find("#close span").text(selectedPointLOL[4]);
		$stocksDisplay.find("#vol span").text(selectedPointLOL[5]);
		$stocksDisplay.find("#stock span").text(allTheStocksData[indexSelected][0]);
		$stocksDisplay.find("#growth span").text(String((intersectedObject.point.z/130.0*100.0).toFixed(2))+"%");
	}
}
document.addEventListener('mousedown',onDocumentMouseDown, false);
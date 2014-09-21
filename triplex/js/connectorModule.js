$(function() {
	$stocksUL = $("#stocksList");
    if(window.getCookie("stocksList")==undefined){
        window.setCookie("stocksList","",20)
    }
    $("#addStockBtn").click(function(){
    	stockN = $("#stockInput").val();
    	if (stockN != ""){
    		//alert(stockN);
    		if(allTheStocks.contain(stockN)==false){
    			allTheStocks.add(stockN);
                ll = allTheStocks.length
                randIndex = Math.floor((Math.random()*colors.length))
                allTheStocksColors.add([colors[randIndex][0],colors[randIndex][1]]);
    			cleanGraph();
    			loadStocks();
    			$stocksUL.append(liString(stockN, allTheStocks.items().length-1));
                $("#stockInput").val("");
    		}
    		else {
    			alert("stock already showing");
    		}

    	}
    	else {
    		alert("No stock was written");
    	}
    	//if ($("#stockInput").val())
        // allTheStocks.add($("#stockInput").val(""));
        // cleanGraph();
        // loadStocks();
        //alert($("#stockInput").val());

    });
    function removeStockFromUL(stockName){
        $(".stocksInList[name='"+stockName+"']").remove();
    }
    function liString(stockName, index){
        //alert(index);
        if(index==undefined){
            index = 0;
        }
        //alert(allTheStocksColors.items()[index][0]);
    	//alert("<li class='stockInList' name='{0}'><div class='colorcube' style='background-color:{1} ;' ></div>{0}  <span class='removeStockInList'><a href='#'>X</a></span></li>".format(stockName, allTheStocksColors.items()[index][0]));
        return "<li class='stockInList' name='{0}'><div class='colorcube' style='background-color:{1} ;' ></div>{0}  <span class='removeStockInList'><a href='#'>X</a></span></li>".format(stockName, allTheStocksColors.items()[index][0]);
    }
    $.each(allTheStocks.items(), function(index, value){
        $stocksUL.append(liString(value, index));
    });
    if(allTheStocks.items().length!=0){
        cleanGraph();
        loadStocks();
    }
    $stocksUL.on('click', '.stockInList .removeStockInList a', function(){
        stockName = $(this).parent().parent().attr('name');
        $(this).parent().parent().remove();
        if(allTheStocks.items().length==1){
            allTheStocksColors.clear();
            allTheStocks.clear();
            cleanGraph();
        }
        else {
            allTheStocksColors.removeVal(allTheStocksColors.items()[allTheStocks.items().indexOf(stockName)]);
            allTheStocks.removeVal(stockName);
            cleanGraph();
            loadStocks();
        }
    });
});
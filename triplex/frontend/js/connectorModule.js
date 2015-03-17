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
    today = new Date();
    $("#toDatePicker").val(String(today.getMonth()+1)+"-"+String(today.getDate())+"-"+String(today.getFullYear()));
    $("#fromDatePicker").val(String(today.getMonth()+1)+"-"+String(today.getDate()-14)+"-"+String(today.getFullYear()));
    refreshDates();
    $("#changeDates").on('click', function(){
        refreshDates();
    });
    function refreshDates(){
        fromDate = $("#fromDatePicker").val().split("-");
        toDate = $("#toDatePicker").val().split("-");
        doIt = false;
        if(parseInt(fromDate[2])<parseInt(toDate[2])){
            doIt = true;
        }
        else if(parseInt(fromDate[2])==parseInt(toDate[2])){
            if(parseInt(fromDate[0])<parseInt(toDate[0])){
                doIt = true;
            }
            else if(parseInt(fromDate[0])==parseInt(toDate[0])){
                if(parseInt(fromDate[1])<parseInt(toDate[1])){
                    doIt = true;
                }
                else {
                    alert("The day is greater or the same")
                }
            }
            else {
                alert("The month of the first date is greater");
            }
        }
        else {
            alert("The year of the first date is greater");
        }
        if(doIt==true){
            //alert("lol");
            cleanGraph();
            loadStocks();
        }
        else {
            alert("non");
        }
    }
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
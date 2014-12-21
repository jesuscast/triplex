/*------------
------------------------------------------------------------
------------------------------------------------------------
------------------------------------------------------------
GLOBAL VARIABLES
------------------------------------------------------------
------------------------------------------------------------
------------------------------------------------------------
*/
var container, scene, camera, renderer, controls, stats, raycaster, projector, allTheLines;
var currentLineIntersected = undefined;
var sphereSelection;
var mouse = new THREE.Vector2();
var clock = new THREE.Clock();
var leftPressed = false;
var rightPressed = false;
var upPressed = false;
var downPressed = false;
var mousePressed = false;
var pointSelected = false;
//for retrieving the stocks
var allTheStocksData = [];
//end for retrieving the stocks
//var pointSelectedCoordinates = new THREE.Vector3(0,0,0);
var intersectedObject = null;
var radiusCamera = 300; //300;
var xCameraPosition = 50;
var yCameraPosition = 50;
var zCameraPosition = 50;
var cameraCenter = new THREE.Vector3(xCameraPosition, yCameraPosition, zCameraPosition);
var pi = 3.14;
var degrees = pi / 180;
var alphaAngle = 270 * degrees; //horizontal
var betaAngle = 180 * degrees; //vertical for 3d
//I put it in 90 degrees so it doesnt add extra cosine
var colors = [["#c0392b",0xc0392b], ["#2c3e50",0x2c3e50], ["#45A300",0x45A300], ["#ACE900",0xACE900], ["#FE4365",0xFE4365], ["#43091F",0x43091F]];

var options = {
    size: 100,
    step: 10
}

allTheLines = new THREE.Object3D();
var particle;
var lol;

Array.prototype.remove = function(from, to) {
    var rest = this.slice((to || from) + 1 || this.length);
    this.length = from < 0 ? this.length + from : from;
    return this.push.apply(this, rest);
};

var stocksArray = new Array();

//var stockIndexes = {};

/*--------------------------- COOKIES-------------------------------------------*/
/*----------------------------------------------------------------------------------*/
/*----------------------------------------------------------------------------------*/
/*----------------------------------------------------------------------------------*/
window.getCookie = function(c_name) {
    var ARRcookies, i, x, y;
    i = void 0;
    x = void 0;
    y = void 0;
    ARRcookies = document.cookie.split(";");
    i = 0;
    while (i < ARRcookies.length) {
        x = ARRcookies[i].substr(0, ARRcookies[i].indexOf("="));
        y = ARRcookies[i].substr(ARRcookies[i].indexOf("=") + 1);
        x = x.replace(/^\s+|\s+$/g, "");
        if (x === c_name) {
            return unescape(y);
        }
        i++;
    }
    if (ARRcookies.length === 1) {
        return null;
    }
};

window.setCookie = function(c_name, value, exdays) {
    var c_value, exdate;
    exdate = new Date();
    exdate.setDate(exdate.getDate() + exdays);
    c_value = escape(value) + (!(exdays != null) ? "" : "; expires=" + exdate.toUTCString()) + "; path=/";
    return document.cookie = c_name + "=" + c_value;
};

window.delCookie = function(c_name) {
    return document.cookie = c_name + "=; expires=Thu, 01 Jan 1970 00:00:01 GMT;";
};




//This is not production quality, its just demo code.
var cookieListFFF = function(cookieName) {
    //When the cookie is saved the items will be a comma seperated string
    //So we will split the cookie by comma to get the original array
    var cookie = $.cookie(cookieName);
    //Load the items or a new array if null.
    var items;
    if (cookie != "") {
        items = cookie ? cookie.split(/,/) : new Array();
    } else {
        items = new Array();
    }

    //Return a object that we can use to access the array.
    //while hiding direct access to the declared items array
    //this is called closures see http://www.jibbering.com/faq/faq_notes/closures.html
    return {
        "add": function(val) {
            //Add to the items.
            items.push(val);
            //Save the items to a cookie.
            //EDIT: Modified from linked answer by Nick see 
            //      http://stackoverflow.com/questions/3387251/how-to-store-array-in-jquery-cookie
            $.cookie(cookieName, items.join(','));
        },
        "remove": function(val) {
                //EDIT: Thx to Assef and luke for remove.
                /** indexOf not support in IE, and I add the below code **/
                if (!Array.prototype.indexOf) {
                    Array.prototype.indexOf = function(obj, start) {
                        for (var i = (start || 0), j = this.length; i < j; i++) {
                            if (this[i] === obj) {
                                return i;
                            }
                        }
                        return -1;
                    }
                }
                var indx = items.indexOf(val);
                if (indx != -1) items.splice(indx, 1);
                //if(indx!=-1) alert('lol');
                $.cookie(cookieName, items.join(','));
            }
            //That the remove method also shims the native Array object is something you wouldn't expect from the remove method. Unexpected side effect. 
            ,
        "clear": function() {
            items = [];
            //clear the cookie.
            $.cookie(cookieName, "");
        },
        "items": function() {
            //Get all the items.
            return items;
        },
        "contain": function(val) {
            //Check if an item is there.
            if (!Array.prototype.indexOf) {
                Array.prototype.indexOf = function(obj, start) {
                    for (var i = (start || 0), j = this.length; i < j; i++) {
                        if (this[i] === obj) {
                            return i;
                        }
                    }
                    return -1;
                };
            }
            var indx = items.join(',').indexOf(val);
            if (indx > -1) {
                return true;
            } else {
                return false;
            }
        }
    }
}

var cookieList = function(cookieName){
  var cookieVals;
  if($.cookie(cookieName)!=undefined){
    cookieVals = JSON.parse($.cookie(cookieName));
  }
  else {
    cookieVals = new Array();
  }
  return {
    'add': function(val){
      cookieVals.push(val);
      $.cookie(cookieName, JSON.stringify(cookieVals));
    },
    'items': function(){
      return cookieVals;
    },
    'removeVal': function(val){
      if(cookieVals.length!=0){
        index = 0;
        for(i=0; i<cookieVals.length; i++){
          if(cookieVals[i]==val){
            index = i;
          }
        }
        cookieVals.remove(index);
        $.cookie(cookieName, JSON.stringify(cookieVals));
      }
    }, 
    'clear': function(){
        cookieVals = new Array();
        $.cookie(cookieName, JSON.stringify(cookieVals));
    },
    'contain': function(val){
      contain = false;
      if(cookieVals.length!=0){
        index = -1;
        for(i=0; i<cookieVals.length; i++){
          if(cookieVals[i]==val){
            index = i;
          }
        }
        if(index!=-1){
          return true;
        }
        else {
          return false;
        }
        //cookieVals.remove(index);
        //$.cookie(cookieName, JSON.stringify(cookieVals));
      }
      else {
        return false;
      }
    }//end ccontain
    }
  }// end return
allTheStocks = new cookieList("allTheStocksL");
allTheStocksColors = new cookieList("allTheStocksColorsL");
//$.cookie("lol","");
// tr = new lol("lo22l");
// //tr.add("1");
// alert(tr.items()[0]);
// // tr.add(["cholo","yolo"]);
// tr.removeVal([1,2]);
// alert(tr.items()[2][1]);

//for modyfing format strings
// First, checks if it isn't implemented yet.
if (!String.prototype.format) {
    String.prototype.format = function() {
        var args = arguments;
        return this.replace(/{(\d+)}/g, function(match, number) {
            return typeof args[number] != 'undefined' ? args[number] : match;
        });
    };
}
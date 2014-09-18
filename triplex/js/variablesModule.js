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
var radiusCamera = 180;
var xCameraPosition = 50;
var yCameraPosition = 50;
var zCameraPosition = 50;
var cameraCenter = new THREE.Vector3(xCameraPosition, yCameraPosition, zCameraPosition);
var pi = 3.14;
var degrees = pi/180;
var alphaAngle = 270*degrees; //horizontal
var betaAngle = 180*degrees; //vertical for 3d
//I put it in 90 degrees so it doesnt add extra cosine

var options = {
	size: 100,
	step: 10
}

allTheLines = new THREE.Object3D();
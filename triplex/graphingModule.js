//Constructor: line
function Line(xArray, yArray, zArray, color){
	//Variables
	if (typeof color === 'undefined') { myVariable = 0x0000ff; }

	this.point = new THREE.Vector3();
	this.direction = new THREE.Vector3();
	this.material = new THREE.LineBasicMaterial({
				color: color
			});
	this.geometry = new THREE.Geometry();
	this.line = null;
	//Inner Functions
	function isArray(myArray) {
		return myArray.constructor.toString().indexOf("Array") > -1;
	}
	//Outer Functions
	this.getLine = function(){
		return this.line;
	}
	//Body
	if(isArray(xArray)==true && isArray(yArray)==true && isArray(zArray)==true){
		if(xArray.length==yArray.length && yArray.length==zArray.length){
			// for(i=0; i<xArray.length; i++){
			// 	this.direction.x = xArray[i];
			// 	this.direction.y = yArray[i];
			// 	this.direction.z = zArray[i];
			// 	this.direction.normalize().multiplyScalar(1);
			// 	this.point.add(direction)
			// }
			for(i=0; i<xArray.length; i++){
				this.geometry.vertices.push(new THREE.Vector3(xArray[i], yArray[i], zArray[i]));
			}
			this.line = new THREE.Line(this.geometry, this.material, THREE.LineStrip);
			//return this.line;
		} else {
			return 0;
		}
	} else {
		return 0;
	}
}

function AxesGrid(size){
	this.lineLength = size;
	this.xAxisX = [0];
	this.xAxisY = [0];
	this.xAxisZ = [0];
	this.yAxisX = [0];
	this.yAxisY = [0];
	this.yAxisZ = [0];
	this.zAxisX = [0];
	this.zAxisY = [0];
	this.zAxisZ = [0];
	for(i=0; i<this.lineLength; i++){
		this.xAxisX[i] = i;
		this.xAxisY[i] = 0;
		this.xAxisZ[i] = 0;

		this.yAxisX[i] = 0;
		this.yAxisY[i] = i;
		this.yAxisZ[i] = 0;

		this.zAxisX[i] = 0;
		this.zAxisY[i] = 0;
		this.zAxisZ[i] = -i;
	}
	this.xAxis = new Line(this.xAxisX, this.xAxisY, this.xAxisZ, 0x0000ff);
	this.yAxis = new Line(this.yAxisX, this.yAxisY, this.yAxisZ, 0xff0000);
	this.zAxis = new Line(this.zAxisX, this.zAxisY, this.zAxisZ, 0x00ff00);


}

var container, scene, camera, renderer, controls, stats;
var clock = new THREE.Clock();

init();
animate();
function init(){
	renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);
    camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 1, 500);
    camera.position.set(50, 50, 130);
    camera.lookAt(new THREE.Vector3(50, 50, 0));
    scene = new THREE.Scene();
    // var line2 = new line([-10, 0, 10],[0, 10, 0],[0,0,0]);
    // var lineLOL = line2.getLine();
    var axisLines = new AxesGrid(100);
	scene.add(axisLines.xAxis.getLine());
    scene.add(axisLines.yAxis.getLine());
    scene.add(axisLines.zAxis.getLine());

	renderer.render(scene, camera);
}

function animate(){
	requestAnimationFrame(animate);
	render();
	update();
}

function update(){
	// if ( keyboard.pressed("z") ){	  
	// 	alert("x="+camera.position.x.toString()+", y="+camera.position.y.toString()+", z="+camera.position.z.toString());
	// }
	// controls.update();

}

function render(){
	renderer.render(scene, camera);
}
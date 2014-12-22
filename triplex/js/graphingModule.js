/*------------
------------------------------------------------------------
------------------------------------------------------------
------------------------------------------------------------
OBJECTS
------------------------------------------------------------
------------------------------------------------------------
------------------------------------------------------------
*/
//Constructor: line
function Line(xArray, yArray, zArray, color) {
    //Variables
    if (typeof color === 'undefined') {
        color = 0x43091F;
    }

    this.point = new THREE.Vector3();
    this.direction = new THREE.Vector3();
    this.material = new THREE.LineBasicMaterial({
        color: color,
        linewidth: 2
    });
    this.geometry = new THREE.Geometry();
    this.line = null;
    //this.indexStock = 0;
    //Private Functions
    function isArray(myArray) {
            return myArray.constructor.toString().indexOf("Array") > -1;
        }
        //Public Functions
    this.getLine = function() {
            return this.line;
        }
        //Body
    if (isArray(xArray) == true && isArray(yArray) == true && isArray(zArray) == true) {
        if (xArray.length == yArray.length && yArray.length == zArray.length) {
            // for(i=0; i<xArray.length; i++){
            // 	this.direction.x = xArray[i];
            // 	this.direction.y = yArray[i];
            // 	this.direction.z = zArray[i];
            // 	this.direction.normalize().multiplyScalar(1);
            // 	this.point.add(direction)
            // }
            for (i = 0; i < xArray.length; i++) {
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

function AxesGrid(size, step) {
        //Private Variables
        var geometry = new THREE.Geometry();
        var material = new THREE.LineBasicMaterial({
            vertexColors: THREE.VertexColors
        });
        var color1 = new THREE.Color(0x87BFDD);
        var color2 = new THREE.Color(0x349FD9);
        var color3 = new THREE.Color(0x1546E8);
        var color4 = new THREE.Color(0x0837D1);
        var color5 = new THREE.Color(0x072CA8);
        var color6 = new THREE.Color(0x06268F);
        //Public Variables
        this.line = null;
        //Private functions
        //..

        //Public Functions
        this.getGrid = function() {
                return this.line;
            }
            //Body

        for (i = 0; i <= size; i += step) {
            //creates the x grid
            geometry.vertices.push(
                new THREE.Vector3(0, 0, i),
                new THREE.Vector3(size, 0, i),
                new THREE.Vector3(i, 0, 0),
                new THREE.Vector3(i, 0, size)
            );
            //creates the z grid
            geometry.vertices.push(
                new THREE.Vector3(0, 0, i),
                new THREE.Vector3(0, size, i),
                new THREE.Vector3(0, i, 0),
                new THREE.Vector3(0, i, size)
            );
            //creates the y grid
            geometry.vertices.push(
                new THREE.Vector3(i, 0, 0),
                new THREE.Vector3(i, size, 0),
                new THREE.Vector3(0, i, 0),
                new THREE.Vector3(size, i, 0)
            );
            var colorX = i === 0 ? color1 : color2;
            var colorY = i === 0 ? color3 : color4;
            var colorZ = i === 0 ? color5 : color6;
            geometry.colors.push(colorX, colorX, colorX, colorX);
            geometry.colors.push(colorY, colorY, colorY, colorY);
            geometry.colors.push(colorZ, colorZ, colorZ, colorZ);
        }
        this.line = new THREE.Line(geometry, material, THREE.LinePieces);
    }

/*------------
------------------------------------------------------------
------------------------------------------------------------
------------------------------------------------------------
GRAPHING FUNCTIONS
------------------------------------------------------------
------------------------------------------------------------
------------------------------------------------------------
*/

function initGraphing() {
    //Set the screen, container, renderer, and scene
    //container = document.createElement( 'div' );
    scene = new THREE.Scene();
    container = $("#graphCanvas");
    renderer = new THREE.WebGLRenderer({ canvas: container.get(0), alpha: true });
    // renderer = new THREE.CanvasRenderer({
    //     canvas: container.get(0)
    // });
    renderer.setSize(container.width(), container.height());
    //container.appendChild(renderer.domElement);
    //document.getElementById('graph').appendChild(renderer.domElement);
    camera = new THREE.PerspectiveCamera(45, container.width() / container.height(), 1, 500);
    setCameraPosition();
    //lollll
    //camera.position.set(150, 150, 500);
    //lollll
    camera.lookAt(cameraCenter);
    camera.rotation.order = 'YXZ';
    scene.add(camera);
    // var size = 100;
    // var step = 10;
    var axesGrid = new AxesGrid(options.size, options.step);
    scene.add(axesGrid.getGrid());
    //Creates the object that is going to hold all lines
    allTheLines = new THREE.Object3D();
    //Create projector for the projector of the plot into the camera
    projector = new THREE.Projector();
    //Add raycaster that is going to gold all the plots
    raycaster = new THREE.Raycaster();
    raycaster.linePrecision = 3;
    //Add sample line
    // var line1 = new Line([0, 20, 50, 100],[0, 20, 50, 100],[0, 20, 70, 80]);
    // allTheLines.add(line1.getLine());
    //Render the scene
    renderer.setClearColor(0xffffff, 1);
    renderer.render(scene, camera);
    //Add Sphere that marks selected line
    var PI2 = Math.PI * 2;
    var programForDrawingSphereSelection = function(context) {

        context.beginPath();
        context.arc(0, 0, 0.5, 0, PI2, true);
        context.fill();

    }
    sphereSelection = new THREE.Sprite(
        new THREE.SpriteCanvasMaterial({
            color: 0xff0000,
            program: programForDrawingSphereSelection
        })
    );
    sphereSelection.scale.x = 5;
    sphereSelection.scale.y = 5;
    //sphereSelection.position.set(50, 50, 50);
    sphereSelection.visible = false;
    scene.add(sphereSelection);
    //Put the allTheLines object into the scene
    scene.add(allTheLines);

    /*

	s
	s
	s
	s
	s
	s
	*/

    function makeTextSprite(text, params) {
        var font = "Arial",
            size = 20,
            color = "#000";
        padding = 0;

        font = "bold " + size + "px " + font;

        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        context.font = font;

        // get size data (height depends only on font size)
        var metrics = context.measureText(text),
            textWidth = metrics.width;

        canvas.width = textWidth + 3;
        canvas.height = size + 3;

        context.font = font;
        context.fillStyle = color;
        context.fillText(text, 0, size + 3);
        //context.style.border="3px solid blue";

        // canvas contents will be used for a texture
        var texture = new THREE.Texture(canvas);
        texture.needsUpdate = true;

        var mesh = new THREE.Mesh(
            new THREE.PlaneGeometry(canvas.width, canvas.height),
            new THREE.MeshBasicMaterial({
                map: texture,
                side: THREE.DoubleSide
            }));
        return mesh;
    }




    xMarks = createText2D('Yield', 'black', null, 30);
    xMarks.position.set(160, 0, 65);
    scene.add(xMarks);

    yMarks = createText2D('competitive margin', 'black', null, 30);
    yMarks.position.set(-20, 65, 130);
    scene.add(yMarks);

    zMarks = createText2D('Time', 'black', null, 30);
    zMarks.position.set(65, -5, 130);
    scene.add(zMarks);

    
    //scene.add(particles);
    //KEYBOARD BINDINGS
    KeyboardJS.on('left', function() {
        leftPressed = true;
    }, function() {
        leftPressed = false;
    });
    KeyboardJS.on('right', function() {
        rightPressed = true;
    }, function() {
        rightPressed = false;
    });
    KeyboardJS.on('up', function() {
        upPressed = true;
    }, function() {
        upPressed = false;
    });
    KeyboardJS.on('down', function() {
        downPressed = true;
    }, function() {
        downPressed = false;
    });
    //MOUSE BINDINGS
    document.addEventListener('mousemove', onDocumentMouseMove, false);

}

function animateGraphing() {
    requestAnimationFrame(animateGraphing);
    if (leftPressed) {
        //camera.rotation.y += 0.01;
        alphaAngle += 0.6 * degrees;
    } else if (rightPressed) {
        //camera.rotation.y -= 0.01;
        alphaAngle -= 0.6 * degrees;
    }
    if (upPressed) {
        //camera.rotation.x += 0.01;
        betaAngle -= 0.6 * degrees;
    } else if (downPressed) {
        //camera.rotation.x -= 0.01;
        betaAngle += 0.6 * degrees;
    }
    setCameraPosition();
    updateGraphing();
    renderGraphing();
}

function updateGraphing() {
    // if ( keyboard.pressed("z") ){	  
    // 	alert("x="+camera.position.x.toString()+", y="+camera.position.y.toString()+", z="+camera.position.z.toString());
    // }
    // controls.update();

}

function renderGraphing() {
        //Find intersections of the mouse and the lines
        var mousePosition = new THREE.Vector3(mouse.x, mouse.y, 1);
        projector.unprojectVector(mousePosition, camera);
        raycaster.set(camera.position, mousePosition.sub(camera.position).normalize());
        var intersects = raycaster.intersectObjects(allTheLines.children, true);
        if (intersects.length > 0) {
            if (currentLineIntersected !== undefined) {
                currentLineIntersected.material.linewidth = 2;
            }
            currentLineIntersected = intersects[0].object;
            currentLineIntersected.material.linewidth = 5;
            sphereSelection.visible = true;
            sphereSelection.position.copy(intersects[0].point);
            pointSelected = true;
            intersectedObject = intersects[0];
        } else {
            if (currentLineIntersected !== undefined) {
                currentLineIntersected.material.linewidth = 2;
            }
            currentLineIntersected = undefined;
            sphereSelection.visible = false;
            pointSelected = false;
            intersectedObject = null;
        }
        xMarks.quaternion.copy( camera.quaternion );
        yMarks.quaternion.copy( camera.quaternion );
        zMarks.quaternion.copy( camera.quaternion );
        renderer.render(scene, camera);
    }
    /*------------
    ------------------------------------------------------------
    ------------------------------------------------------------
    ------------------------------------------------------------
    ADDITIONAL FUNCTIONS
    ------------------------------------------------------------
    ------------------------------------------------------------
    ------------------------------------------------------------
    */

function onDocumentMouseMove() {
    event.preventDefault();
    mouse.x = ((event.clientX - container.offset().left) / container.width()) * 2 - 1;
    mouse.y = -((event.clientY - container.offset().top) / container.height()) * 2 + 1;
    //sprite1.position.set( event.clientX, event.clientY - 20, 0 );
}

function setCameraPosition() {
    camera.position.set(xCameraPosition + radiusCamera * (Math.cos(alphaAngle) * Math.cos(betaAngle)), yCameraPosition + radiusCamera * Math.sin(betaAngle), zCameraPosition + radiusCamera * (Math.cos(betaAngle) * Math.sin(alphaAngle)));
    camera.lookAt(cameraCenter);
    //the sin(alphaAngle) is negative because the z axis runs positive downwards (towards us)
    //sprite1.position.set( event.clientX, event.clientY - 20, 0 );
}


function createTextCanvas(text, color, font, size) {

    size = size || 24;
    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');
    var fontStr = (size + 'px ') + (font || 'Arial');
    ctx.font = fontStr;
    var w = ctx.measureText(text).width;
    var h = Math.ceil(size);
    if(w>100){
        canvas.width = 160;
    canvas.height = 60;

    ctx.font = fontStr;
    ctx.textAlign = 'center';
    ctx.fillStyle = color || 'black';
    ctx.fillText("competitive", 80, Math.ceil(size * 0.8));
    ctx.fillText("margin", 80, Math.ceil(size * 0.8)+28);
    }
    else {
    canvas.width = w;
    canvas.height = h;

    ctx.font = fontStr;

    ctx.fillStyle = color || 'black';
    ctx.fillText(text, 0, Math.ceil(size * 0.8));
    }
    return canvas;

}

function createText2D(text, color, font, size, segW, segH) {

    var canvas = createTextCanvas(text, color, font, size);
    var plane = new THREE.PlaneGeometry(canvas.width, canvas.height, segW, segH);
    var tex = new THREE.Texture(canvas);

    tex.needsUpdate = true;

    var planeMat = new THREE.MeshBasicMaterial({
        map: tex,
        color: 0xffffff,
        transparent: true
    });

    var mesh = new THREE.Mesh(plane, planeMat);
    mesh.scale.set(0.2, 0.2, 0.2);
    //mesh.doubleSided = true; // this is no longer a property of mesh // CHANGED
    //mesh.quaternion = camera.quaternion; // CHANGED
    mesh.quaternion.copy( camera.quaternion );
    //mesh.quaternion(new THREE.Vecto3(xCameraPosition + radiusCamera * (Math.cos(alphaAngle) * Math.cos(betaAngle)), yCameraPosition + radiusCamera * Math.sin(betaAngle), zCameraPosition + radiusCamera * (Math.cos(betaAngle) * Math.sin(alphaAngle))));
    return mesh;

}

let renderer, scene, camera, mixer, markerRoot;

let clock, deltaTime, totalTime;

let arToolkitSource, arToolkitContext;


if (document.explora_ar_context){
    initialize();
    animate();
} else {
    console.log("No explora AR context found, scene not initialized");
}


function initialize(){

	renderer = new THREE.WebGLRenderer({
		antialias : true,
		// alpha: true,
		preserveDrawingBuffer: true 
	});

	renderer.setClearColor(new THREE.Color('lightgrey'), 0)
	renderer.setSize( window.innerWidth, window.innerHeight );
	renderer.domElement.style.position = 'absolute'
	renderer.domElement.style.top = '0px'
	renderer.domElement.style.left = '0px'
	document.getElementById("container").appendChild( renderer.domElement );
	
	scene = new THREE.Scene();

	let ambientLight = new THREE.AmbientLight( 0xffffff, 0.5 );
    scene.add( ambientLight );

    const light = new THREE.HemisphereLight( 0xffffbb, 0x080820, 1.2 );
    scene.add( light );
				
	camera = new THREE.Camera();
	scene.add(camera);


	clock = new THREE.Clock();
	deltaTime = 0;
	totalTime = 0;

	document.explora_ar_context.animation_mixers = [];

	////////////////////////////////////////////////////////////
	// setup LoadingManager
	////////////////////////////////////////////////////////////
	document.explora_ar_context.load_errors = [];
	document.explora_ar_context.loading_div = document.getElementById('loading');
	document.explora_ar_context.load_bar = document.querySelector("#load_bar>div");
	document.explora_ar_context.load_span = document.getElementById("load_resource");
	document.explora_ar_context.error_div = document.querySelector("#loading .errors");


	THREE.DefaultLoadingManager.onLoad = () => {
		document.explora_ar_context.load_span.innerHTML = "Complete!";
		document.explora_ar_context.loading_div.classList.add("load_complete");
		document.getElementById("overlay").classList.remove("infohidden");
		console.log(`THREE Resources loading Complete!`);
	};

	THREE.DefaultLoadingManager.onProgress = (u, p, t) => {
		let percent = Math.min(100*p/t, 100);
		document.explora_ar_context.load_bar.style.width = `${percent}%`;  
		document.explora_ar_context.load_span.innerHTML = u;
		console.log(`Loaded ${u}, ${p}/${t} ${percent.toFixed(1)}`);
	};

	THREE.DefaultLoadingManager.onError = (u) => {
		document.explora_ar_context.error_div.style.display = 'block';
		if (! document.explora_ar_context.load_errors.includes(u)){
			document.explora_ar_context.load_errors.push(u);
			let el = document.createElement('p');
			el.innerHTML = u;
			document.explora_ar_context.error_div.append(el);
		}
		document.explora_ar_context.loading_div.style.transitionDelay = "3s"
		console.log(`Error loading ${u}`);
	};

	
	////////////////////////////////////////////////////////////
	// setup arToolkitSource
	////////////////////////////////////////////////////////////

	arToolkitSource = new THREEx.ArToolkitSource({
		// to read from the webcam
		sourceType: 'webcam',

		sourceWidth: window.innerWidth > window.innerHeight ? 640 : 480,
		sourceHeight: window.innerWidth > window.innerHeight ? 480 : 640,

	});


	
	arToolkitSource.init(function onReady() {
		let vid = document.querySelector("body video");
		vid.remove();
		document.getElementById("container").appendChild( vid );
		
		arToolkitSource.domElement.addEventListener('canplay', () => {
			console.log(
				'canplay',
				'actual source dimensions',
				arToolkitSource.domElement.videoWidth,
				arToolkitSource.domElement.videoHeight
			);

			document.explora_ar_context.load_span.innerHTML = "Camera started";
			document.explora_ar_context.loading_div.classList.remove("wait-camera");

			initARContext();
		});
		window.arToolkitSource = arToolkitSource;
		setTimeout(() => {
			onResize()
		}, 2000);
	})

	// handle resize
	window.addEventListener('resize', function () {
		onResize()
	})

	function onResize() {
		arToolkitSource.onResizeElement()
		arToolkitSource.copyElementSizeTo(renderer.domElement)
		if (window.arToolkitContext.arController !== null) {
			arToolkitSource.copyElementSizeTo(window.arToolkitContext.arController.canvas)
		}
	}
	
	////////////////////////////////////////////////////////////
	// setup arToolkitContext
	////////////////////////////////////////////////////////////	

	function initARContext() { // create atToolkitContext
		arToolkitContext = new THREEx.ArToolkitContext({
			cameraParametersUrl: document.explora_ar_context.cameraParametersUrl ,
			detectionMode: 'mono_and_matrix',
			debug: document.explora_ar_context.debug
		})
		// initialize it
		arToolkitContext.init(() => { // copy projection matrix to camera
			camera.projectionMatrix.copy(arToolkitContext.getProjectionMatrix());

			arToolkitContext.arController.orientation = getSourceOrientation();
			arToolkitContext.arController.options.orientation = getSourceOrientation();

			console.log('arToolkitContext', arToolkitContext);
			window.arToolkitContext = arToolkitContext;

			setupPhotoBtn(renderer.domElement);
			setupInfoDiv();
			setupMarkerRoots();
		})

	}

	function getSourceOrientation() {
		if (!arToolkitSource) {
			return null;
		}

		console.log(
			'actual source dimensions',
			arToolkitSource.domElement.videoWidth,
			arToolkitSource.domElement.videoHeight
		);

		if (arToolkitSource.domElement.videoWidth > arToolkitSource.domElement.videoHeight) {
			console.log('source orientation', 'landscape');
			return 'landscape';
		} else {
			console.log('source orientation', 'portrait');
			return 'portrait';
		}
	}


	function setupPhotoBtn(canvas){
		let photoBtn = document.querySelector("#buttons .photo_btn");
		const photo_img = document.querySelector("#photo_div img");
		const photo_a = document.querySelector("#photo_div a");

		photoBtn.addEventListener("click", (e)=>{

			const screenshotTarget = document.getElementById("container");
			console.log(screenshotTarget);

			html2canvas(screenshotTarget).then((canvas) => {
				const img = canvas.toDataURL('image/jpeg');
				// SIMULATE A LINK CLICK TO DOWNLOAD
				// Construct the 'a' element
				var link = document.createElement("a");
				let date= new Date().toISOString().slice(0,-5).replace(":","-");
				link.download = `Explora_AR-${date}.jpg`;
				link.target = "_blank";
			
				// Construct the URI
				link.href = img;
				document.body.appendChild(link);
				link.click();
			
				// Cleanup the DOM
				document.body.removeChild(link);
				delete link;
			});


		});
	}

	let visible_markers = {};

	function setupInfoDiv(){
		let objs = document.explora_ar_context.objects;
		let infodiv = document.querySelector("#info>div");
		let btndiv = document.querySelector("#buttons>div");

		let infop = document.querySelector("#info .text_container");
		let closeBtn = document.querySelector("#info .close_btn");
		let infoBtn = document.querySelector("#buttons .info_btn");

		let userHide = false;

		closeBtn.addEventListener("click", (e)=>{
			userHide = true;
			infodiv.classList.add("infohidden");
			btndiv.classList.remove("raise");
			infoBtn.classList.remove("infohidden");
		})

		infoBtn.addEventListener("click", (e)=>{
			userHide = false;
			btndiv.classList.add("raise");
			infodiv.classList.remove("infohidden");
			infoBtn.classList.add("infohidden");
		})

		window.addEventListener("markerLost", (e)=>{
			let id = e.detail.id;
			
			visible_markers[id] = false;
			setTimeout(() => {
				// console.log("HIDE EVENT Timeout: " + userHide, visible_markers);
	
				btndiv.classList.remove("raise");
				if (userHide) {
					infoBtn.classList.add("infohidden");
				} else if (!visible_markers[id]){
					infodiv.classList.add("infohidden");
				} 
			}, 1000);
		})

		window.addEventListener("markerFound", (e)=>{ 
			
			let id = e.detail.id;
			infop.innerHTML = htmlDecode(objs[id]["info"]);
			if (!visible_markers[id]){
				visible_markers[id] = true;
				setTimeout(() => {
					// console.log("SHOW Event Timeout: " + userHide, visible_markers);
					if (userHide) {
						infoBtn.classList.remove("infohidden");
					} else if (visible_markers[id]){
						infodiv.classList.remove("infohidden");
						btndiv.classList.add("raise");

					} 
				}, 1000);
			}
		});
	} 


	////////////////////////////////////////////////////////////
	// setup markerRoots
	////////////////////////////////////////////////////////////

	function setupMarkerRoots(){
		// let geometry1 = new THREE.PlaneGeometry(1,1, 4,4);
		// let material1 = new THREE.MeshBasicMaterial( { color: 0x0000ff, opacity: 0.5 } );
		
		let objs = document.explora_ar_context.objects;
		
		for (let i = 0; i < objs.length; i++) {
			let ar_obj = objs[i];
			visible_markers[i] = false;

			ar_obj["markerRoot"] = new THREE.Group();
			scene.add(ar_obj["markerRoot"]);
			ar_obj['markerControls'] = new THREEx.ArMarkerControls(window.arToolkitContext, ar_obj["markerRoot"], {
				type: 'barcode', barcodeValue: ar_obj["barcodeValue"],
			})

			// ar_obj["debugMesh"] = new THREE.Mesh( geometry1, material1 );
			// ar_obj["debugMesh"].rotation.x = -Math.PI/2;
			// ar_obj["markerRoot"].add( ar_obj["debugMesh"] );

			console.log(`Setting up slot [${ar_obj.slot}], marker #${ar_obj.barcodeValue}, file: ${ar_obj.modelPath}`)

			load_gltf(ar_obj, ar_obj["markerRoot"], true);
		
		} // end for
	}
	


} // end initialize()




function update()
{
	// console.log(!arToolkitContext, !arToolkitSource, !arToolkitSource.ready)
	// update artoolkit on every frame
	if (!arToolkitContext || !arToolkitSource || !arToolkitSource.ready) {
		return;
	}
	
	arToolkitContext.update( arToolkitSource.domElement );
	
	if (THREE.stats) THREE.stats.update();
}


function render()
{
	renderer.render( scene, camera );
}


function animate()
{
	requestAnimationFrame(animate);
	deltaTime = clock.getDelta();
	totalTime += deltaTime;

	document.explora_ar_context.animation_mixers.forEach((m) => {
		m.update(deltaTime);
	});

	update();
	render();
}
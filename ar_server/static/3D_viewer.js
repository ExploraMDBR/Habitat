let renderer, scene, camera, mixer, markerRoot;
let animationLoop;
let container;
let model;



function init3DViewer(domElem, item){
    if (renderer) return;
    container = domElem;

    
    let markerPath = item["markerImage"];

    let positionInfo = container.getBoundingClientRect();
    let height = positionInfo.height;
    let width = positionInfo.width;

    console.log(`INIT 3D viewer (${width}x${height})in:`, container);

    renderer = new THREE.WebGLRenderer({
        antialias : true,
        alpha: false
    });

    renderer.setClearColor(new THREE.Color(0xcccccc), 1)
    renderer.setSize( width, height);
    domElem.appendChild( renderer.domElement );

    scene = new THREE.Scene();

    let ambientLight = new THREE.AmbientLight( 0xffffff, 0.5 );
    scene.add( ambientLight );

    const light = new THREE.HemisphereLight( 0xffffbb, 0x080820, 1.2 );
    scene.add( light );

    const loader = new THREE.CubeTextureLoader();
    loader.setPath( '/static/bg/' );
    textureCube = loader.load( [ 'posx.jpg', 'negx.jpg', 'posy.jpg', 'negy.jpg', 'posz.jpg', 'negz.jpg' ] );
    scene.background = textureCube;
    
    camera = new THREE.PerspectiveCamera( 50, width/height, 0.1, 100 );
    camera.position.x = 0.2;
    camera.position.y = 1.5;
    camera.position.z = 2.5;

    cameraRoot = new THREE.Group();
    camera.lookAt(0,0.5,-1);
    cameraRoot.add(camera);
    scene.add(cameraRoot);

    console.log(scene);

    clock = new THREE.Clock();
    deltaTime = 0;
    totalTime = 0;

    markerRoot = new THREE.Group();

    const textureLoader = new THREE.TextureLoader();
    const texture1 = textureLoader.load( markerPath );
    let geometry1 = new THREE.PlaneGeometry(1,1, 4,4);
    let material1 = new THREE.MeshBasicMaterial( { color: 'white', map: texture1 } );
    let mesh = new THREE.Mesh( geometry1, material1 );
    mesh.rotation.x = -Math.PI/2;
    markerRoot.add(mesh)
    
    const texture_ground = textureLoader.load( '/static/bg/negy.jpg' );
    let material_ground = new THREE.MeshBasicMaterial( { color: 'white', map: texture_ground } );
    let geometry_ground = new THREE.PlaneGeometry(10,10, 4,4);
    let mesh_ground = new THREE.Mesh( geometry_ground, material_ground );
    mesh_ground.rotation.x = -Math.PI/2;
    mesh_ground.position.y = -0.1;
    markerRoot.add(mesh_ground);

    scene.add(markerRoot)
    
    load_gltf(item, markerRoot);

    let t = 0
    requestAnimationFrame(function animate(nowMsec) {
        animationLoop =  requestAnimationFrame(animate);
        renderer.render(scene, camera);
        let deltaTime = clock.getDelta();
        t += deltaTime
        cameraRoot.rotation.y = t/5;
        if (mixer) mixer.update( deltaTime );
    })
}

function remove3DViewer(){
    if (!renderer) return;
    cancelAnimationFrame(animationLoop);
    renderer.domElement.remove();
    renderer = undefined;
}
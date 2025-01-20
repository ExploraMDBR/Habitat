function set_loc_scale(x,y,z, scale){
    if (!model) return;
    model.scale.copy(new THREE.Vector3(scale, scale, scale));
    model.position.x = x;
    model.position.y = y;
    model.position.z = z;
}

function load_gltf(item, markerRoot, push_mixer = false ){
    const gltfLoader = new THREE.GLTFLoader();
    let gltfPath = item["modelPath"];
    gltfLoader.load(gltfPath, (gltf) => {
        model = gltf.scene;
        markerRoot.add(model);
        set_loc_scale(item.position.x, item.position.y, item.position.z, item.scale.x);

        if (item.default) {
            console.log("DEFAULT Model:", item.slot)
            model.children.forEach((child) => {
                if (child.name == "Empty_numbers"){
                    child.children.forEach((number)=>{
                        if (number.name != `${item.slot}`){
                            number.visible = false;
                        }
                    });
                }
            });
        }
        
        if (gltf.animations.length > 0){
            mixer = new THREE.AnimationMixer( model );
            mixer.clipAction( gltf.animations[ 0 ] ).play();
            if (push_mixer) document.explora_ar_context.animation_mixers.push(mixer);
        }
    });

}

function htmlDecode(input) {
    var doc = new DOMParser().parseFromString(input, "text/html");
    return doc.documentElement.textContent;
}
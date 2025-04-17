import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector("#bg"),
    antialias: true,
    powerPreference: "high-performance"

});
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.alpha = true; // Allow transparent backgrounds,

// Camera position
// camera.position.setX: 0.07077528096286616;
// camera.position.setY: 3.1174571145005934;
// camera.position.setZ: 14.730626104688032;
camera.position.set(0, 5, 10); // Adjusted to better view the model

// Add OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);
// controls.enableDamping = true; // Adds smooth damping effect
// controls.dampingFactor = 0.05;

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
// directionalLight.position.set(5, 5, 5);
// directionalLight.castShadow = true;
// directionalLight.shadow.mapSize.width = 2048;
// directionalLight.shadow.mapSize.height = 2048;
scene.add(directionalLight);

// Optional light helper
// const lightHelper = new THREE.DirectionalLightHelper(directionalLight);
const gridHelper = new THREE.GridHelper(100,50);
// scene.add(gridHelper);

// Load model
const gltfLoader = new GLTFLoader();
const initialCameraPos = {
        "x": 0.2473485458374758,
        "y": -1.314966939167312,
        "z": 18.50482797979478
};

// Set the look-at target (adjust these values to focus where you want)
const lookAtTarget = new THREE.Vector3(0, 1.5, 0); // Looking slightly downward

// In your model load callback:
gltfLoader.load(
    '/cau-genai/dev_scripts/sekani_scripts/models/ship.glb',
    (gltf) => {
        const model = gltf.scene;
        scene.add(model);

        // Set camera to precise starting position
        camera.position.set(initialCameraPos.x, initialCameraPos.y, initialCameraPos.z);
        camera.lookAt(lookAtTarget);
        
        // Configure controls to maintain this view
        controls.target.copy(lookAtTarget);
        controls.update();
        
        // Optional: Add slight damping for smooth movement
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;
        
        // Optional: Limit camera movement ranges
        controls.minDistance = 10;  // Minimum zoom distance
        controls.maxDistance = 20;  // Maximum zoom distance
        controls.maxPolarAngle = Math.PI * 0.6; // Limit looking downward
        
        console.log("Camera initialized at:", camera.position);
    },
    undefined,
    (error) => console.error('Error loading model:', error)
);
// gltfLoader.load(
//     '/cau-genai/dev_scripts/sekani_scripts/models/ship.glb',
//     (gltf) => {
//         const model = gltf.scene;
//         scene.add(model);

//         model.traverse(child => {
//         if (child.isMesh) {
//             child.castShadow = true;
//             child.receiveShadow = true;
//         }
//     });

//         // 1. Find cockpit position (adjust these values)
//         const cockpitPosition = new THREE.Vector3(0, 1.5, -3); // Example values
//         const lookAtPosition = new THREE.Vector3(0, 1.5, 10); // Looking forward

//         // 2. Set camera to cockpit view
//         camera.position.copy(cockpitPosition);
//         camera.lookAt(lookAtPosition);
//         controls.target.copy(lookAtPosition);
//         controls.update();

//         // 3. Limit controls to prevent clipping through walls
//         controls.minDistance = 1; // Minimum zoom distance
//         controls.maxDistance = 5; // Maximum zoom distance
//         controls.maxPolarAngle = Math.PI * 0.5; // Limit looking straight down

//         // 4. Add debug markers (remove in production)
//         const cockpitMarker = new THREE.Mesh(
//             new THREE.SphereGeometry(0.1, 16, 16),
//             new THREE.MeshBasicMaterial({ color: 0xff0000 })
//         );
//         cockpitMarker.position.copy(cockpitPosition);
//         scene.add(cockpitMarker);

//         const lookAtMarker = new THREE.Mesh(
//             new THREE.SphereGeometry(0.1, 16, 16),
//             new THREE.MeshBasicMaterial({ color: 0x00ff00 })
//         );
//         lookAtMarker.position.copy(lookAtPosition);
//         scene.add(lookAtMarker);
//     },
//     undefined,
//     (error) => console.error('Error:', error)
// );

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    controls.update(); // Required for damping to work
    renderer.render(scene, camera);


    // Add to your animate() function
    window.addEventListener('keydown', (e) => {
        const step = 0.1;
        switch(e.key) {
            case 'ArrowUp': camera.position.y += step; break;
            case 'ArrowDown': camera.position.y -= step; break;
            case 'ArrowLeft': camera.position.x -= step; break;
            case 'ArrowRight': camera.position.x += step; break;
            case 'w': camera.position.z += step; break;
            case 's': camera.position.z -= step; break;
        }
        console.log('Camera position:', camera.position);
    });
}
animate();

// Background (optional)
// const spaceTexture = new THREE.TextureLoader().load('/cau-genai/dev_scripts/sekani_scripts/static/img/bkg4.jpeg');
// scene.background = spaceTexture;

// Handle window resizing
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});



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

// Set initial camera position
const initialCameraPos = {
    x: 0.2473485458374758,
    y: -1.314966939167312,
    z: 18.50482797979478
};
camera.position.set(initialCameraPos.x, initialCameraPos.y, initialCameraPos.z);

// Add OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1.5, 0);
controls.update();

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 5.0);
scene.add(ambientLight);
const directionalLight = new THREE.DirectionalLight(0xffffff, 5.0);
directionalLight.position.set(1, 1, 1).normalize();
scene.add(directionalLight);

// Create screen plane
const screenGeometry = new THREE.PlaneGeometry(33, 9);
// const screenMaterial = new THREE.MeshBasicMaterial({ 
//     color: 0x111111,
//     side: THREE.DoubleSide
// });
// const screen = new THREE.Mesh(screenGeometry, screenMaterial);
// screen.position.set(0, 1.8, -0.3);
// scene.add(screen);






// Now load your texture - add this right after creating the screen





// Model reference
let model = null;

// Load model
const gltfLoader = new GLTFLoader();
const gltfLoader2 = new GLTFLoader();
gltfLoader.load(
    '/cau-genai/dev_scripts/sekani_scripts/models/ship.glb',
    (gltf) => {
        model = gltf.scene;
        scene.add(model);
        model.position.set(0, 0, 0);
    },
    undefined,
    (error) => console.error('Error loading model:', error)
);

gltfLoader2.load(
    '/cau-genai/dev_scripts/sekani_scripts/models/helmet.glb',
    (gltf) => {
        model = gltf.scene;
        scene.add(model);
        model.position.set(0, 0, -15);
    },
    undefined,
    (error) => console.error('Error loading model:', error)
);

const spaceTexture = new THREE.TextureLoader().load('/cau-genai/dev_scripts/sekani_scripts/static/img/bkg.jpg')
scene.background = spaceTexture;

// Animation variables - increased speeds
let time = 0;
const rockingSpeed = 1.0; // Increased from 0.5 (2x faster)
const rockingAmount = 0.08; // Slightly increased movement
const flyingSpeed = 0.8; // New separate speed control

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    
    if (model) {
        time += 0.01;

        // Faster wave patterns
        const wave1 = Math.sin(time * rockingSpeed * 1.2);
        const wave2 = Math.cos(time * rockingSpeed * 0.8);
        const wave3 = Math.sin(time * rockingSpeed * 1.5);

        // Apply more pronounced rotations
        model.rotation.x = (wave1 * 0.03) + (wave2 * 0.02); // Increased from 0.02/0.01
        model.rotation.y = (wave2 * 0.05) + (wave3 * 0.02); // Increased from 0.03/0.01
        model.rotation.z = (wave1 * 0.01) + (wave3 * 0.01); // Increased from 0.005

        // More noticeable vertical movement
        model.position.y = (wave1 + wave3) * 0.15; // Increased from 0.1

        // Horizontal movement with different timing
        model.position.x = Math.sin(time * flyingSpeed) * 0.08; // Increased from 0.05
    }

    controls.update();
    renderer.render(scene, camera);
}
animate();



// Handle window resizing
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
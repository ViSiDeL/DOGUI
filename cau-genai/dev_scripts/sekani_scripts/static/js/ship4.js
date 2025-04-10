import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { CSS3DRenderer, CSS3DObject } from 'three/addons/renderers/CSS3DRenderer.js';

// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector("#bg"),
    antialias: true,
    powerPreference: "high-performance"
});
// HTML Renderer
const cssRenderer = new CSS3DRenderer();
cssRenderer.setSize(window.innerWidth, window.innerHeight);
cssRenderer.domElement.style.position = 'absolute';
cssRenderer.domElement.style.top = '0';
cssRenderer.domElement.style.pointerEvents = 'none';
document.body.appendChild(cssRenderer.domElement);
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
const screenMaterial = new THREE.TextureLoader().load('./static/img/bkg.jpg')
const screen = new THREE.Mesh(
    new THREE.PlaneGeometry(50, 20),
    new THREE.MeshBasicMaterial({ map: screenMaterial})
);
screen.position.set(0, 3.8, -9.9);
scene.add(screen);

// Model reference
let model = null;

// Create iframe element
const iframe = document.createElement('iframe');
iframe.src = 'http://127.0.0.1:5500/dev_scripts/sekani_scripts/test.html'; // Your webpage URL
iframe.style.width = '2048px';
iframe.style.height = '768px';
iframe.style.border = 'none';
iframe.style.backgroundColor = '#000';

// Create CSS3DObject
const htmlScreen = new CSS3DObject(iframe);
htmlScreen.scale.set(0.02, 0.02, 0.02); // Adjust scale as needed
htmlScreen.position.set(0, 1.8, -0.3); // Same position as your plane
htmlScreen.rotation.set(0, Math.PI, 0); // Adjust rotation to face camera
scene.add(htmlScreen);

// Load model
const gltfLoader = new GLTFLoader();
const gltfLoader2 = new GLTFLoader();
gltfLoader.load(
    './models/ship.glb',
    (gltf) => {
        model = gltf.scene;
        scene.add(model);
        model.position.set(0, 0, 0);
    },
    undefined,
    (error) => console.error('Error loading model:', error)
);

gltfLoader2.load(
    './models/helmet.glb',
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
    cssRenderer.render(scene, camera);
}
animate();



// Handle window resizing
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    cssRenderer.setSize(window.innerWidth, window.innerHeight);
});
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

// Camera position
camera.position.set(0, 5, 10); // Adjusted to better view the model

// Add OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true; // Adds smooth damping effect
controls.dampingFactor = 0.05;

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(5, 5, 5);
scene.add(directionalLight);

// Optional light helper
// const lightHelper = new THREE.DirectionalLightHelper(directionalLight);
const gridHelper = new THREE.GridHelper(100,50);
// scene.add(gridHelper);

// Load model
const gltfLoader = new GLTFLoader();
gltfLoader.load(
    '/cau-genai/dev_scripts/sekani_scripts/models/ship.glb',
    (gltf) => {
        const model = gltf.scene;

        // Center and scale model if needed
        const box = new THREE.Box3().setFromObject(model);
        const center = box.getCenter(new THREE.Vector3());
        model.position.sub(center);

        // Optional: Adjust model scale
        // model.scale.set(0.1, 0.1, 0.1);

        scene.add(model);

        // Optional: Position camera based on model size
        // const size = box.getSize(new THREE.Vector3());
        // camera.position.z = size.length() * 1.5;
    },
    undefined,
    (error) => {
        console.error('Error loading model:', error);
    }
);

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    controls.update(); // Required for damping to work
    renderer.render(scene, camera);
}
animate();

// Background (optional)
const spaceTexture = new THREE.TextureLoader().load('/cau-genai/dev_scripts/sekani_scripts/static/img/bkg4.jpeg');
scene.background = spaceTexture;

// Handle window resizing
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});


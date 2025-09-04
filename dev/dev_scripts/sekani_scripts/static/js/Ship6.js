import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { CSS3DRenderer, CSS3DObject } from 'three/addons/renderers/CSS3DRenderer.js';

import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'three/addons/postprocessing/UnrealBloomPass.js';


// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

// Main WebGL Renderer
const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector("#bg"),
    antialias: true,
    alpha: true
});
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);

// CSS3D Renderer for HTML content
const cssRenderer = new CSS3DRenderer();
cssRenderer.setSize(window.innerWidth, window.innerHeight);
cssRenderer.domElement.style.position = 'absolute';
cssRenderer.domElement.style.top = '0';
cssRenderer.domElement.style.pointerEvents = 'none'; // Allow interaction
document.body.appendChild(cssRenderer.domElement);

// Camera setup
camera.position.set(0.247, -1.315, 18.505);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 1.5, 0);

//Glow set up
const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new UnrealBloomPass(new THREE.Vector2(window.innerWidth, window.innerHeight), 1.2, 0.4, 0.85));


// Lighting - reduced intensity
const ambientLight = new THREE.DirectionalLight(0xffffff, 0.5);
scene.add(ambientLight);

const hemiLight = new THREE.HemisphereLight(0x88ccff, 0x110033, 0.6); // Sky + ground tones
scene.add(hemiLight);


// Background
new THREE.TextureLoader().load('./static/img/bkg.jpg', texture => {
    scene.background = texture;
});

// HTML Screen Setup
function createHTMLScreen() {
    const iframe = document.createElement('iframe');
    iframe.src = './dogui/templates/index.html';
    iframe.style.width = '1024px';
    iframe.style.height = '768px';
    iframe.style.border = 'none';
    iframe.style.backgroundColor = '#000';

    // Handle iframe loading
    iframe.onload = () => console.log('HTML screen loaded');
    iframe.onerror = () => console.error('Failed to load HTML screen');

    const htmlScreen = new CSS3DObject(iframe);
    htmlScreen.scale.set(0.02, 0.02, 0.02);
    htmlScreen.position.set(0, 1.8, -50.3);
    htmlScreen.rotation.set(0, Math.PI, 0); // Face the camera

    return htmlScreen;
}

const htmlScreen = createHTMLScreen();
scene.add(htmlScreen);

// Ship Model
const gltfLoader = new GLTFLoader();
let shipModel = null;

gltfLoader.load('./models/ship9.glb', (gltf) => {
    shipModel = gltf.scene;
    shipModel.position.set(0, 0, 0);
    scene.add(shipModel);
    // Start animation only after model loads
    animate();
}, undefined, (error) => {
    console.error('Error loading ship:', error);
});

// Animation variables
let time = 0;
const rockingSpeed = 1.0;

// Animation Loop
function animate() {
    requestAnimationFrame(animate);

    if (shipModel) {
        time += 0.01;
        const wave1 = Math.sin(time * rockingSpeed * 1.2);
        const wave2 = Math.cos(time * rockingSpeed * 0.8);

        shipModel.rotation.set(
            wave1 * 0.03,
            wave2 * 0.05,
            wave1 * 0.01
        );
        shipModel.position.y = wave1 * 0.;
    }

    controls.update();
    renderer.render(scene, camera);
    cssRenderer.render(scene, camera);
}

// Handle Resizing
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
    cssRenderer.setSize(window.innerWidth, window.innerHeight);
});
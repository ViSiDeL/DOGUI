import * as THREE from "three";
import {OrbitControls} from "three-orbitcontrols";

let mouseX = 0;
let mouseY = 0;
let targetX = 0;
let targetY = 0;
const smoothingFactor = 0.5;

// Track mouse movement
document.addEventListener('mousemove', (event) => {
    mouseX = (event.clientX / window.innerWidth) * 2 - 1; 
    mouseY = -(event.clientY / window.innerHeight) * 2 + 1;
});


// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true });  // Transparent background
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.domElement.style.position = 'fixed'; 
renderer.domElement.style.top = '0';
renderer.domElement.style.left = '0';
renderer.domElement.style.zIndex = '4'; 
// renderer.domElement.style.pointerEvents = 'auto';
renderer.domElement.style.pointerEvents = 'none';
document.body.appendChild(renderer.domElement);

// Cube setup
const geometry = new THREE.BoxGeometry(2, 2, 2);
// const material = new THREE.MeshBasicMaterial({ color: 0x000000, wireframe: true });
const material = new THREE.MeshStandardMaterial({
    color: 0x3e947e,    // Solid black
    roughness: 0.8,      // Matte-like surface
    metalness: 0.1       // Slight reflectiveness
});
const cube = new THREE.Mesh(geometry, material);
cube.position.y -= 1.2
scene.add(cube);

camera.position.z = 5;

// Ambient light (global lighting)
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);  
scene.add(ambientLight);

// Directional light (simulates sunlight)
const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(20, 20, 20).normalize();
scene.add(directionalLight);

// const controls = new OrbitControls(camera, renderer.domElement);
// controls.enableDamping = true;  // Smooth interaction

// Adjust camera position based on mouse movement
function updateCameraPosition() {
    // Change the camera position based on mouseX and mouseY
    camera.position.x = -(mouseX * 0.20);  // Adjust this factor for more/less movement
    camera.position.y = -(mouseY * 0.20);  // Adjust this factor for more/less movement
}

// Animation loop with camera update
function animate() {
    requestAnimationFrame(animate);

    // Update camera position
    updateCameraPositionSmooth();

    // Rotate the cube (optional)
    cube.rotation.x += 0.01;  
    cube.rotation.y += 0.01;

    // Render the scene
    renderer.render(scene, camera);
}
animate();

// Smooth camera movement
function updateCameraPositionSmooth() {
    targetX = -mouseX * 1;  // Target X position based on mouse
    targetY = -mouseY * 1;  // Target Y position based on mouse

    // Smooth the movement
    camera.position.x += (targetX - camera.position.x) * smoothingFactor;
    camera.position.y += (targetY - camera.position.y) * smoothingFactor;
}

// Background Music SetUp

<audio src="/music/good_enough.mp3" controls>
<p>If you are reading this, it is because your browser does not support the audio element.</p>
</audio>


// Handle window resizing
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

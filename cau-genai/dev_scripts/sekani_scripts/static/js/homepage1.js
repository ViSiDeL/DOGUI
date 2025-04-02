import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Scene setup
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({
    canvas: document.querySelector("#bg"),
});
renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize(window.innerWidth, window.innerHeight);
camera.position.setZ(30);

// Add OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);

// Torus setup
const geometry = new THREE.BoxGeometry(10,10,10);
const material = new THREE.MeshBasicMaterial({
    color: 0xFF6347,
    wireframe: true
});
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// Lighting
const pointLight = new THREE.PointLight(0xffffff);
pointLight.position.set(5, 5, 5);
scene.add(pointLight);

// Ambient light for even illumination
const ambientLight = new THREE.AmbientLight(0x404040);
scene.add(ambientLight);

const lightHelper = new THREE.PointLightHelper(pointLight);
const gridHelper = new THREE.GridHelper(200,50);
scene.add(lightHelper);

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.005;
    cube.rotation.z += 0.01;
    
    controls.update();
    renderer.render(scene, camera);
}
animate();

//  Add stars
function addStar(){
    const geometry = new THREE.Geometry(0.25, 24, 24);
    const material = new THREE.MeshStandardMaterial( {color: 0xffffff})
    const star = new THREE.Mesh(geometry, material);

    const[x,y,z] = Array(3).fill().map(() => THREE.MathUtils.randFloatSpread(100));

    star.position.set(x, y, z);
    scene.add(star);
}

Array(200).fill.forEach(addStar);

// Handle window resizing
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

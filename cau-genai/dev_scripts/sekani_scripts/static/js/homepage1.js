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

// Torus setup - 10,3,16,100
const geometry = new THREE.BoxGeometry(10,10,10);
const material = new THREE.MeshStandardMaterial({
    color: 0x3e947e,
    // wireframe: true
});
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);

// Lighting
const pointLight = new THREE.PointLight(0xffffff);
pointLight.position.set(5, 5, 5);
// scene.add(pointLight);

// Ambient light for even illumination
const ambientLight = new THREE.DirectionalLight(0xffffff);
scene.add(pointLight, ambientLight);

const lightHelper = new THREE.PointLightHelper(pointLight);
const gridHelper = new THREE.GridHelper(100,50);
// scene.add(gridHelper)

// cube.position.z=30;
// cube.position.setX(0)

function moveCamera() {
    const t = document.body.getBoundingClientRect().top;

    cube.rotation.x += 5.05;
    cube.rotation.y += 5.075;
    cube.rotation.z += 5.05;




    camera.position.z = t * -0.055;
    camera.position.y = t * -0.055;
    camera.position.x = t * -0.055;
}

document.body.onscroll = moveCamera()

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
    const geometry = new THREE.SphereGeometry(0.15, 24, 24);
    const material = new THREE.MeshStandardMaterial( {color: 0xffffff})
    const star = new THREE.Mesh(geometry, material);

    const[x, y, z] = Array(3).fill().map(() => THREE.MathUtils.randFloatSpread(100));

    star.position.set(x, y, z);
    scene.add(star);
}

Array(750).fill().forEach(addStar);


const spaceTexture = new THREE.TextureLoader().load('/cau-genai/dev_scripts/sekani_scripts/static/img/bkg.jpg')
scene.background = spaceTexture;
// Handle window resizing
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

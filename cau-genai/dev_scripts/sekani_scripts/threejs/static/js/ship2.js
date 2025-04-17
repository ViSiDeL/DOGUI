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

camera.position.set(0, 5, 10); // Adjusted to better view the model

// Add OrbitControls
const controls = new OrbitControls(camera, renderer.domElement);

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
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

// Screen Manager Class
class ShipScreens {
    constructor() {
      this.screens = [];
      this.currentFocus = null;
    }
  
    addScreen(mesh, type, contentCallback) {
      const screen = {
        mesh,
        type,
        content: new THREE.Group(),
        update: contentCallback
      };
      this.screens.push(screen);
      mesh.add(screen.content);
      return screen;
    }
  
    updateAll() {
      this.screens.forEach(screen => {
        if (screen.update) screen.update(screen.content);
      });
    }
  }

const shipScreens = new ShipScreens();

// Circular Radar Screen
function createRadarScreen() {
    const geometry = new THREE.CircleGeometry(0, 32);
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00, side: THREE.DoubleSide });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(-2, 1.5, -0.5); // Position in cockpit

    shipScreens.addScreen(mesh, 'radar', (content) => {
      // Clear previous frame
      content.children = [];

      // Radar circles
      for (let i = 1; i <= 3; i++) {
        const circle = new THREE.Line(
          new THREE.BufferGeometry().setFromPoints(
            new THREE.EllipseCurve(0, 0, i * 0.3, i * 0.3).getPoints(64)
          ),
          new THREE.LineBasicMaterial({ color: 0x00ff00 })
        );
        content.add(circle);
      }

      // Sweeping line
      const angle = Date.now() * 0.002;
      const line = new THREE.Line(
        new THREE.BufferGeometry().setFromPoints([
          new THREE.Vector3(0, 0, 0),
          new THREE.Vector3(Math.cos(angle) * 1, Math.sin(angle) * 1, 0)
        ]),
        new THREE.LineBasicMaterial({ color: 0x00ff00 })
      );
      content.add(line);

      // Random blips
      if (Math.random() > 0.7) {
        const blip = new THREE.Mesh(
          new THREE.CircleGeometry(0.05, 8),
          new THREE.MeshBasicMaterial({ color: 0xff0000 })
        );
        blip.position.set(
          (Math.random() - 0.5) * 1.8,
          (Math.random() - 0.5) * 1.8,
          0
        );
        content.add(blip);
      }
    });
}

// Main Info Screen
function createMainScreen() {
    const geometry = new THREE.PlaneGeometry(30, 8, 3, 3);
    const material = new THREE.MeshBasicMaterial({ color: 0x111111});
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(0, 1.8, -0.3);

    // HTML Overlay Element
    const screenElement = document.createElement('div');
    screenElement.className = 'ship-screen';
    screenElement.innerHTML = `
      <div class="screen-header">SYSTEM STATUS</div>
      <div class="screen-metric">SPEED: <span id="speed-value">217</span> m/s</div>
      <div class="screen-metric">SHIELDS: <span id="shields-value">100</span>%</div>
    `;
    document.body.appendChild(screenElement);

    // Position tracking
    mesh.userData.updatePosition = () => {
      const vector = mesh.position.clone()
        .applyMatrix4(mesh.matrixWorld)
        .project(camera);

      screenElement.style.transform = `translate(
        ${(vector.x * 0.5 + 0.5) * window.innerWidth - 150}px,
        ${(-vector.y * 0.5 + 0.5) * window.innerHeight - 75}px
      )`;
    };

    // Animated values
    setInterval(() => {
      document.getElementById('speed-value').textContent = 
        Math.floor(217 + Math.random() * 3);
      document.getElementById('shields-value').textContent = 
        Math.floor(100 - Math.random() * 2);
    }, 1000);

    return mesh;
}

// Clickable Screen Areas
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function onMouseClick(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(
    shipScreens.screens.map(s => s.mesh)
  );

  if (intersects.length > 0) {
    const screen = shipScreens.screens.find(
      s => s.mesh === intersects[0].object
    );

    // Pulse animation
    gsap.to(screen.mesh.material, {
      emissiveIntensity: 2,
      duration: 0.3,
      yoyo: true,
      repeat: 1
    });

    // Screen-specific actions
    if (screen.type === 'radar') {
      alert('Radar system engaged!');
    }
  }
}
// In your model load callback:
gltfLoader.load(
    '/cau-genai/dev_scripts/sekani_scripts/models/ship.glb',
    (gltf) => {
        const model = gltf.scene;
        scene.add(model);
        

        // Create screens
        createRadarScreen();
        const mainScreen = createMainScreen();
        model.add(mainScreen);

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

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    controls.update(); // Required for damping to work
    // Update all screens
    shipScreens.updateAll();
    
    // Update HTML screen positions
    shipScreens.screens.forEach(screen => {
        if (screen.mesh.userData.updatePosition) {
        screen.mesh.userData.updatePosition();
        }
    });
    


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

    renderer.render(scene, camera);
}
animate();

// Background (optional)
// const spaceTexture = new THREE.TextureLoader().load('/cau-genai/dev_scripts/sekani_scripts/static/img/bkg4.jpeg');
// scene.background = spaceTexture;

// Handle window resizing
window.addEventListener('click', onMouseClick, false);
window.addEventListener('scroll', updateCameraPosition);
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});



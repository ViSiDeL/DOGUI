// generation.js - Handles Three.js scene and AI generation
import * as THREE from "three";
import {OrbitControls} from "three-orbitcontrols";

class ModelGenerator {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.grid = null;
    }
    
    initThreeJS() {
        // scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xf0f0f0);
        
        // camera
        this.camera = new THREE.PerspectiveCamera(
            50, 
            window.innerWidth / window.innerHeight, 
            0.1, 
            2000
        );
        this.camera.position.z = 15;
        
        // renderer
        const canvas = document.getElementById('threejs-canvas');
        this.renderer = new THREE.WebGLRenderer({ 
            canvas, 
            antialias: true 
        });
        
        // orbit controls
        this.controls = new OrbitControls(
            this.camera, 
            this.renderer.domElement
        );
        
        // lighting
        const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
        directionalLight.position.set(2, 1, 1);
        this.scene.add(directionalLight);
        
        this.scene.add(new THREE.AmbientLight(0x404040));
        
        // grid
        this.grid = new THREE.GridHelper(10, 10)
        this.grid.position.y = -3 
        this.scene.add(this.grid);
        
        // animation loop
        const animate = () => {
            requestAnimationFrame(animate);
            this.controls.update();
            this.renderer.render(this.scene, this.camera);
        };
        animate();
        
        // Handle window resize
        window.addEventListener('resize', () => {
            this.camera.aspect = canvas.parentElement.clientWidth / canvas.parentElement.clientHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(
                canvas.parentElement.clientWidth, 
                canvas.parentElement.clientHeight
            );
        });
    }
    
    setupUI() {
        document.getElementById('generate-btn').addEventListener('click', () => {
            const description = document.getElementById('description').value.trim();
            if (!description) {
                alert('Please enter a description');
                return;
            }
            
            this.generateModel(description);
        });
    }
    
    async generateModel(description) {
        const statusElement = document.getElementById('status');
        statusElement.textContent = 'Generating model...';
        statusElement.style.color = 'inherit';
        
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ description })
            });
            
            const data = await response.json();
            
            if (data.status === 'error') {
                throw new Error(data.error);
            }

            console.log(data)
            
            this.executeGeneratedCode(data.code);
            statusElement.textContent = 'Model generated successfully!';
            statusElement.style.color = 'green';
        } catch (error) {
            statusElement.textContent = `Error: ${error.message}`;
            statusElement.style.color = 'red';
            console.error('Generation error:', error);
        }
    }
    
    executeGeneratedCode(code) {
        // Clear previous model objects (keep lights and helpers)
        this.scene.children = this.scene.children.filter(obj => 
            obj.isLight || obj.isGridHelper || this.grid == obj
        );
        
        try {
            // Create a wrapper function that provides THREE context
            const wrapperFn = new Function(
                'THREE',
                'scene',
                'camera',
                'renderer',
                `
                // Start of generated code execution
                try {
                    ${code}
                } catch(e) {
                    console.error('Execution error in generated code:', e);
                    throw e;
                }
                `
            );
            
            // Execute with proper context
            wrapperFn(
                THREE,          // Provide THREE as parameter
                this.scene, 
                this.camera, 
                this.renderer
            );
        } catch (error) {
            console.error('Code execution error:', error);
            throw new Error(`Failed to execute generated code: ${error.message}`);
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    var generator = new ModelGenerator();
    generator.initThreeJS();
    generator.setupUI();
});
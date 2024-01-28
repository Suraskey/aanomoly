import * as THREE from './static/three.min.js';
import { OrbitControls } from './static/OrbitControls.js';

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('model-viewer').appendChild(renderer.domElement);

const loader = new THREE.OBJLoader();
loader.load('./airplane engine/airplane engine.obj', function(object) { // Adjust path if needed
    scene.add(object);

    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableZoom = false;

    animate();
});

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

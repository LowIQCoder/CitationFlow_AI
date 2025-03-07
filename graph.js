function generateMockData(numOfPoints) {
    return {
        nodes: d3.range(numOfPoints).map(i => {
            const position = new THREE.Vector3(
                (Math.random() - 0.5) * numOfPoints,
                (Math.random() - 0.5) * 5,
                (Math.random() - 0.5) * numOfPoints
            );
            return {
                url: `https://www.sciencedirect.com/science/article/pii/${Math.random().toString(36).substr(2)}`,
                title: `Research Paper ${i + 1}`,
                popular: Math.floor(Math.random() * 1000) + 100,
                position: position
            };
        })
    };
}

function assignColorFromPosition(position) {
    const colorScaleX = d3.scaleSequential(d3.interpolateRainbow).domain([-50, 50]);
    const colorScaleY = d3.scaleSequential(d3.interpolatePlasma).domain([-50, 50]);
    const colorScaleZ = d3.scaleSequential(d3.interpolateViridis).domain([-50, 50]);

    const xColor = d3.color(colorScaleX(position.x));
    const yColor = d3.color(colorScaleY(position.y));
    const zColor = d3.color(colorScaleZ(position.z));

    return d3.rgb(
        (xColor.r + yColor.r + zColor.r) / 3,
        (xColor.g + yColor.g + zColor.g) / 3,
        (xColor.b + yColor.b + zColor.b) / 3
    ).hex();
}

function findClosestNodes(nodes) {
    const edges = [];
    nodes.forEach((node, i) => {
        let closest = null;
        let closestDist = Infinity;
        nodes.forEach((otherNode, j) => {
            if (i !== j) {
                const dist = node.position.distanceTo(otherNode.position);
                if (dist < closestDist) {
                    closestDist = dist;
                    closest = j;
                }
            }
        });
        if (closest !== null) {
            edges.push({ source: i, target: closest });
        }
    });
    return edges;
}

function init(numOfPoints) {
    window.location.reload();
}

document.getElementById('pointsSlider').addEventListener('input', function () {
    const value = this.value;
    document.getElementById('pointsValue').textContent = value;
});

document.getElementById('applyButton').addEventListener('click', function () {
    const value = document.getElementById('pointsSlider').value;
    localStorage.setItem('numOfPoints', value);
    init(Number(value));
});

const savedPoints = localStorage.getItem('numOfPoints') || 20;
document.getElementById('pointsSlider').value = savedPoints;
document.getElementById('pointsValue').textContent = savedPoints;

let scene, camera, renderer, controls, nodes = [], edges = [];
const data = generateMockData(Number(savedPoints));
scene = new THREE.Scene();
camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

camera.position.z = 50;
controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;

nodes = data.nodes.map(node => {
    const geometry = new THREE.SphereGeometry(Math.sqrt(node.popular) / 30, 32, 32);
    const material = new THREE.MeshBasicMaterial({ color: assignColorFromPosition(node.position) });
    const sphere = new THREE.Mesh(geometry, material);
    sphere.position.copy(node.position);
    sphere.userData = node;
    return sphere;
});

edges = findClosestNodes(nodes).map(({ source, target }) => {
    const geometry = new THREE.BufferGeometry().setFromPoints([
        nodes[source].position,
        nodes[target].position
    ]);
    return new THREE.Line(
        geometry,
        new THREE.LineBasicMaterial({ color: 0xaaaaaa, transparent: true, opacity: 0.2 })
    );
});

nodes.forEach(node => scene.add(node));
edges.forEach(edge => scene.add(edge));

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}
animate();
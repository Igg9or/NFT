class NFT3DViewer {
    constructor(containerId, modelUrl) {
        this.container = document.getElementById(containerId);
        this.modelUrl = modelUrl;
        this.init();
    }

    init() {
        // Инициализация Three.js сцены
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, this.container.clientWidth / this.container.clientHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.container.appendChild(this.renderer.domElement);

        // Загрузка модели
        const loader = new THREE.GLTFLoader();
        loader.load(this.modelUrl, (gltf) => {
            this.model = gltf.scene;
            this.scene.add(this.model);
            this.animate();
        });

        // Настройка освещения и камеры
        const light = new THREE.AmbientLight(0xffffff, 0.5);
        this.scene.add(light);
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(0, 1, 1);
        this.scene.add(directionalLight);
        this.camera.position.z = 5;
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        if (this.model) this.model.rotation.y += 0.01;
        this.renderer.render(this.scene, this.camera);
    }
}
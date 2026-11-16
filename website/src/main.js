import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

// =====================================
// 1. 기본 설정
// =====================================

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x9ec9e8);
scene.fog = new THREE.Fog(0x9ec9e8, 80, 250);

const camera = new THREE.PerspectiveCamera(
    60,
    window.innerWidth / window.innerHeight,
    0.1,
    500
);

camera.position.set(0, 8, 15);

const renderer = new THREE.WebGLRenderer({
    antialias: true
});

renderer.setSize(
    window.innerWidth,
    window.innerHeight
);

renderer.setPixelRatio(
    Math.min(window.devicePixelRatio, 2)
);

renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

document.body.appendChild(renderer.domElement);

// =====================================
// 2. 조명
// =====================================

const ambientLight = new THREE.HemisphereLight(
    0xffffff,
    0x667788,
    2
);

scene.add(ambientLight);

const sunlight = new THREE.DirectionalLight(
    0xffffff,
    2.5
);

sunlight.position.set(-20, 40, 20);
sunlight.castShadow = true;
scene.add(sunlight);

// =====================================
// 3. 도로와 주변 환경
// =====================================

const roadMaterial = new THREE.MeshStandardMaterial({
    color: 0x30343a,
    roughness: 0.9
});

const road = new THREE.Mesh(
    new THREE.BoxGeometry(7, 0.1, 240),
    roadMaterial
);

road.position.set(0, -0.08, -100);
road.receiveShadow = true;
scene.add(road);

const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(300, 300),
    new THREE.MeshStandardMaterial({
        color: 0x63865b
    })
);

ground.rotation.x = -Math.PI / 2;
ground.position.y = -0.15;
ground.position.z = -100;
ground.receiveShadow = true;
scene.add(ground);

// 중앙 노란색 차선
function createLine(x, color, width) {
    const line = new THREE.Mesh(
        new THREE.BoxGeometry(width, 0.025, 240),
        new THREE.MeshStandardMaterial({
            color
        })
    );

    line.position.set(x, 0, -100);
    scene.add(line);

    return line;
}

createLine(0, 0xffd900, 0.12);

// 도로 바깥쪽 흰색 선
createLine(-3.45, 0xffffff, 0.1);
createLine(3.45, 0xffffff, 0.1);

// 차선 점선
for (let z = 0; z > -240; z -= 8) {
    const dash = new THREE.Mesh(
        new THREE.BoxGeometry(0.08, 0.025, 4),
        new THREE.MeshStandardMaterial({
            color: 0xffffff
        })
    );

    dash.position.set(0, 0.01, z);
    scene.add(dash);
}

// =====================================
// 4. 주변 건물과 나무
// =====================================

function createBuilding(x, z, width, height, depth) {
    const building = new THREE.Mesh(
        new THREE.BoxGeometry(width, height, depth),
        new THREE.MeshStandardMaterial({
            color: 0x9aa5ad
        })
    );

    building.position.set(
        x,
        height / 2 - 0.1,
        z
    );

    building.castShadow = true;
    building.receiveShadow = true;

    scene.add(building);
}

function createTree(x, z) {
    const trunk = new THREE.Mesh(
        new THREE.CylinderGeometry(0.15, 0.2, 2),
        new THREE.MeshStandardMaterial({
            color: 0x654321
        })
    );

    trunk.position.set(x, 0.9, z);
    scene.add(trunk);

    const leaves = new THREE.Mesh(
        new THREE.SphereGeometry(1.1, 12, 12),
        new THREE.MeshStandardMaterial({
            color: 0x287a3c
        })
    );

    leaves.position.set(x, 2.2, z);
    leaves.castShadow = true;
    scene.add(leaves);
}

for (let z = 0; z > -220; z -= 25) {
    createBuilding(-9, z, 5, 8 + Math.random() * 8, 8);
    createBuilding(9, z - 10, 5, 7 + Math.random() * 10, 8);

    createTree(-5.5, z - 8);
    createTree(5.5, z - 18);
}

// =====================================
// 5. 자동차 생성
// =====================================

function createTrafficCar(color) {
    const group = new THREE.Group();

    const body = new THREE.Mesh(
        new THREE.BoxGeometry(1.7, 0.7, 3.5),
        new THREE.MeshStandardMaterial({
            color,
            roughness: 0.5
        })
    );

    body.position.y = 0.65;
    body.castShadow = true;
    group.add(body);

    const cabin = new THREE.Mesh(
        new THREE.BoxGeometry(1.35, 0.65, 1.7),
        new THREE.MeshStandardMaterial({
            color: 0x252d36
        })
    );

    cabin.position.set(0, 1.25, -0.15);
    group.add(cabin);

    return group;
}

// =====================================
// 6. 보행자 생성
// =====================================

function createPedestrian() {
    const group = new THREE.Group();

    const body = new THREE.Mesh(
        new THREE.CylinderGeometry(0.22, 0.28, 1.0),
        new THREE.MeshStandardMaterial({
            color: 0xff8c00
        })
    );

    body.position.y = 1.0;
    group.add(body);

    const head = new THREE.Mesh(
        new THREE.SphereGeometry(0.23, 16, 16),
        new THREE.MeshStandardMaterial({
            color: 0xffd2a6
        })
    );

    head.position.y = 1.7;
    group.add(head);

    return group;
}

// =====================================
// 7. 자전거 생성
// =====================================

function createBicycle() {
    const group = new THREE.Group();

    const wheelMaterial = new THREE.MeshStandardMaterial({
        color: 0x222222
    });

    for (const z of [-0.65, 0.65]) {
        const wheel = new THREE.Mesh(
            new THREE.TorusGeometry(0.35, 0.045, 8, 20),
            wheelMaterial
        );

        wheel.rotation.y = Math.PI / 2;
        wheel.position.set(0, 0.4, z);
        group.add(wheel);
    }

    const frame = new THREE.Mesh(
        new THREE.BoxGeometry(0.08, 0.08, 1.1),
        new THREE.MeshStandardMaterial({
            color: 0x1677ff
        })
    );

    frame.position.y = 0.75;
    group.add(frame);

    return group;
}

// =====================================
// 8. 주행 차량 GT3 모델
// =====================================

const egoCar = new THREE.Group();
scene.add(egoCar);

const fallbackCar = createTrafficCar(0x1677ff);
egoCar.add(fallbackCar);

const loader = new GLTFLoader();

loader.load(
    '/models/gt3.glb',
    (gltf) => {
        egoCar.remove(fallbackCar);

        const model = gltf.scene;

        model.scale.set(1, 1, 1);
        model.rotation.y = Math.PI;

        model.traverse((child) => {
            if (child.isMesh) {
                child.castShadow = true;
                child.receiveShadow = true;
            }
        });

        egoCar.add(model);
    },
    undefined,
    (error) => {
        console.error('GT3 모델 로딩 실패:', error);
    }
);

// =====================================
// 9. 교통 객체 관리
// =====================================

const trafficObjects = new Map();

function getTrafficObject(obj) {
    if (trafficObjects.has(obj.id)) {
        return trafficObjects.get(obj.id);
    }

    let model;

    if (obj.type === 'pedestrian') {
        model = createPedestrian();
    } else if (obj.type === 'bicycle') {
        model = createBicycle();
    } else {
        model = createTrafficCar(0x777777);
    }

    scene.add(model);
    trafficObjects.set(obj.id, model);

    return model;
}

function updateTraffic(traffic) {
    for (const obj of traffic) {
        const model = getTrafficObject(obj);

        // Python x = 진행 방향
        // Python y = 좌우 방향
        model.position.set(
            obj.y,
            0,
            -obj.x
        );

        if (obj.type === 'pedestrian') {
            model.rotation.y = obj.direction < 0 ? 0 : Math.PI;
        }
    }
}

// =====================================
// 10. 경로 시각화
// =====================================

const pathObjects = new Map();

let currentPathFrame = -1;

function clearPaths() {
    for (const object of pathObjects.values()) {
        scene.remove(object.line);
        object.line.geometry.dispose();
        object.line.material.dispose();
    }

    pathObjects.clear();
}

function updatePaths(frame, frameIndex) {
    if (currentPathFrame === frameIndex) {
        return;
    }

    currentPathFrame = frameIndex;

    clearPaths();

    const trajectories = frame.trajectories;

    if (!trajectories) return;

    for (const [name, points] of Object.entries(trajectories)) {
        if (!points || points.length < 2) continue;

        const positions = [];

        for (const point of points) {
            positions.push(
                new THREE.Vector3(
                    point.y,
                    0.16,
                    -point.x
                )
            );
        }

        const geometry = new THREE.BufferGeometry()
            .setFromPoints(positions);

        const isSelected = name === frame.selected_path;

        const material = new THREE.LineBasicMaterial({
            color: isSelected ? 0x00ff66 : 0xffa500,
            linewidth: 2,
            transparent: true,
            opacity: isSelected ? 1 : 0.35
        });

        const line = new THREE.Line(
            geometry,
            material
        );

        scene.add(line);

        pathObjects.set(name, {
            line,
            anchorX: frame.ego.x,
            anchorY: frame.ego.y
        });
    }
}

function movePathsWithCar(ego) {
    for (const object of pathObjects.values()) {
        object.line.position.set(
            ego.y - object.anchorY,
            0,
            -(ego.x - object.anchorX)
        );
    }
}

// =====================================
// 11. 시뮬레이션 데이터
// =====================================

let frames = [];

let playing = true;
let playbackPosition = 0;
let lastAnimationTime = 0;

const frameInterval = 100;

async function loadSimulationData() {
    try {
        const response = await fetch(
            '/simulation_data.json',
            { cache: 'no-store' }
        );

        if (!response.ok) {
            throw new Error('시뮬레이션 데이터 로딩 실패');
        }

        const data = await response.json();

        frames = data.frames || data;

        if (!frames.length) {
            throw new Error('프레임 데이터가 비어 있음');
        }

        console.log('시뮬레이션 프레임:', frames.length);

        updateSimulation(0);
        animate();

    } catch (error) {
        console.error(error);

        const status = document.getElementById('status');

        if (status) {
            status.textContent = '데이터 로딩 실패';
        }
    }
}

// =====================================
// 12. 프레임 보간
// =====================================

function interpolateValue(a, b, t) {
    return a + (b - a) * t;
}

function interpolateFrame(index, alpha) {
    const current = frames[index];

    // 마지막 프레임에서 첫 프레임으로 보간하지 않음
    if (index >= frames.length - 1) {
        return current;
    }

    const next = frames[index + 1];

    const ego = {
        x: interpolateValue(
            current.ego.x,
            next.ego.x,
            alpha
        ),
        y: interpolateValue(
            current.ego.y,
            next.ego.y,
            alpha
        ),
        speed: interpolateValue(
            current.ego.speed,
            next.ego.speed,
            alpha
        )
    };

    const traffic = current.traffic.map((obj) => {
        const nextObj = next.traffic.find(
            item => item.id === obj.id
        );

        if (!nextObj) return obj;

        return {
            ...obj,
            x: interpolateValue(obj.x, nextObj.x, alpha),
            y: interpolateValue(obj.y, nextObj.y, alpha)
        };
    });

    return {
        ...current,
        ego,
        traffic
    };
}

// =====================================
// 13. HUD
// =====================================

function updateHUD(frame) {
    const timeElement = document.getElementById('time');
    const speedElement = document.getElementById('speed');
    const selectedElement = document.getElementById('selected');
    const statusElement = document.getElementById('status');

    if (timeElement) {
        timeElement.textContent =
            `${frame.time.toFixed(1)} s`;
    }

    if (speedElement) {
        speedElement.textContent =
            `${(frame.ego.speed * 3.6).toFixed(1)} km/h`;
    }

    if (selectedElement) {
        const labels = {
            keep_speed: '속도 유지',
            slow_down: '감속',
            change_lane: '차선 내 회피',
            stop: '비상 정지'
        };

        selectedElement.textContent =
            labels[frame.selected_path] ||
            frame.selected_path;
    }

    if (statusElement) {
        statusElement.textContent =
            frame.selected_path === 'stop'
                ? '안전 경로 없음 - 정지'
                : '주행 중';
    }
}

// =====================================
// 14. 시뮬레이션 업데이트
// =====================================

function updateSimulation(index, alpha = 0) {
    const frame = interpolateFrame(index, alpha);

    // Python 결과를 그대로 반영
    egoCar.position.set(
        frame.ego.y,
        0,
        -frame.ego.x
    );

    updateTraffic(frame.traffic);

    updatePaths(frames[index], index);

    // 경로가 자동차를 따라오도록 이동
    movePathsWithCar(frame.ego);

    updateHUD(frame);

    updateCamera(frame);
}

// =====================================
// 15. 카메라 모드
// =====================================

let cameraMode = 'follow';

function updateCamera(frame) {
    const carX = frame.ego.y;
    const carZ = -frame.ego.x;

    if (cameraMode === 'follow') {
        const targetPosition = new THREE.Vector3(
            carX,
            7,
            carZ + 13
        );

        camera.position.lerp(
            targetPosition,
            0.08
        );

        camera.lookAt(
            carX,
            0,
            carZ - 8
        );

    } else if (cameraMode === 'top') {
        camera.position.set(
            carX,
            30,
            carZ + 2
        );

        camera.lookAt(
            carX,
            0,
            carZ - 10
        );

    } else if (cameraMode === 'driver') {
        camera.position.set(
            carX,
            2.1,
            carZ - 0.5
        );

        camera.lookAt(
            carX,
            1.8,
            carZ - 15
        );
    }
}

// =====================================
// 16. 재생 / 정지 / 초기화
// =====================================

document.getElementById('playBtn')?.addEventListener(
    'click',
    () => {
        playing = true;
        lastAnimationTime = 0;
    }
);

document.getElementById('pauseBtn')?.addEventListener(
    'click',
    () => {
        playing = false;
    }
);

document.getElementById('resetBtn')?.addEventListener(
    'click',
    () => {
        playbackPosition = 0;
        playing = true;
        lastAnimationTime = 0;
        updateSimulation(0);
    }
);

// =====================================
// 17. 카메라 버튼
// =====================================

document.getElementById('followBtn')?.addEventListener(
    'click',
    () => {
        cameraMode = 'follow';
    }
);

document.getElementById('topBtn')?.addEventListener(
    'click',
    () => {
        cameraMode = 'top';
    }
);

document.getElementById('driverBtn')?.addEventListener(
    'click',
    () => {
        cameraMode = 'driver';
    }
);

// =====================================
// 18. 애니메이션
// =====================================

function animate(timestamp = 0) {
    requestAnimationFrame(animate);

    if (playing && frames.length > 1) {
        if (lastAnimationTime === 0) {
            lastAnimationTime = timestamp;
        }

        const delta = timestamp - lastAnimationTime;

        playbackPosition += delta / frameInterval;

        lastAnimationTime = timestamp;

        // 마지막 프레임에 도달하면 처음부터 재생
        if (playbackPosition >= frames.length - 1) {
            playbackPosition = 0;
        }

        const index = Math.floor(playbackPosition);
        const alpha = playbackPosition - index;

        updateSimulation(index, alpha);
    }

    renderer.render(scene, camera);
}

// =====================================
// 19. 화면 크기 변경
// =====================================

window.addEventListener('resize', () => {
    camera.aspect =
        window.innerWidth / window.innerHeight;

    camera.updateProjectionMatrix();

    renderer.setSize(
        window.innerWidth,
        window.innerHeight
    );

    renderer.setPixelRatio(
        Math.min(window.devicePixelRatio, 2)
    );
});

// =====================================
// 20. 시작
// =====================================

loadSimulationData();
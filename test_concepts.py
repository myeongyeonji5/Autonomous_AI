
from simulation.cwnet_environment import CWNetEnvironment
from model.cwnet.trajectory_generator import TrajectoryGenerator
from model.cwnet.concept_classifier import ConceptClassifier

# 1. 가상 도로 생성
env = CWNetEnvironment()
scene = env.reset(seed=42)

# 2. 후보 경로 생성
generator = TrajectoryGenerator()
trajectories = generator.generate(scene["ego"])

# 3. 개념 분류
classifier = ConceptClassifier()

concepts = classifier.classify(
    trajectories,
    scene["traffic"]
)

# 4. 결과 출력
for name, values in concepts.items():

    print(f"\n===== {name} =====")

    for concept, value in values.items():
        print(f"{concept}: {value}")

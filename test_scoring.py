
from simulation.cwnet_environment import CWNetEnvironment
from model.cwnet.trajectory_generator import TrajectoryGenerator
from model.cwnet.concept_classifier import ConceptClassifier
from model.cwnet.scoring_model import TrajectoryScorer

env = CWNetEnvironment()
scene = env.reset(seed=42)

generator = TrajectoryGenerator()
trajectories = generator.generate(scene["ego"])

classifier = ConceptClassifier()
concepts = classifier.classify(
    trajectories, scene["traffic"]
)

scorer = TrajectoryScorer()
scores = scorer.score(trajectories, concepts)
best = scorer.select_best(scores)

for name, values in scores.items():
    print(f"\n===== {name} =====")
    for key, value in values.items():
        print(f"{key}: {value}")

print("\n최종 선택 경로:", best)

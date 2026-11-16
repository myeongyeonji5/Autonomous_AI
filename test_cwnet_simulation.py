import csv
import json
import os

from simulation.cwnet_environment import CWNetEnvironment
from model.cwnet.trajectory_generator import TrajectoryGenerator
from model.cwnet.concept_classifier import ConceptClassifier
from model.cwnet.scoring_model import TrajectoryScorer


env = CWNetEnvironment()
env.reset(seed=42)

generator = TrajectoryGenerator()
classifier = ConceptClassifier()
scorer = TrajectoryScorer()

os.makedirs("results", exist_ok=True)
os.makedirs("website/public", exist_ok=True)

csv_path = "results/cwnet_simulation.csv"
json_path = "website/public/simulation_data.json"

frames = []

SAFE_DISTANCE = 3.0


def is_path_inside_lane(path, ego_y):
    min_y, max_y = generator.get_safe_bounds(ego_y)

    for point in path:
        if point["y"] < min_y or point["y"] > max_y:
            return False

    return True


with open(
    csv_path,
    "w",
    newline="",
    encoding="utf-8-sig"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "step",
        "time",
        "x",
        "y",
        "speed",
        "selected_path",
        "safety_score",
        "efficiency_score",
        "total_score",
        "minimum_distance"
    ])

    for step in range(100):

        scene = env.get_scene()

        trajectories = generator.generate(
            scene["ego"]
        )

        concepts = classifier.classify(
            trajectories,
            scene["traffic"]
        )

        scores = scorer.score(
            trajectories,
            concepts
        )

        # 안전한 경로만 후보로 인정
        safe_candidates = []

        for name, path in trajectories.items():

            inside_lane = is_path_inside_lane(
                path,
                scene["ego"]["y"]
            )

            minimum_distance = concepts[name][
                "minimum_distance"
            ]

            if (
                inside_lane
                and minimum_distance >= SAFE_DISTANCE
            ):
                safe_candidates.append(name)

        # 안전 경로가 있으면 그중 최고 점수 선택
        if safe_candidates:
            best = max(
                safe_candidates,
                key=lambda name: scores[name]["total_score"]
            )

        # 안전 경로가 하나도 없다면 비상 정지
        else:
            best = "stop"

        next_point = trajectories[best][1]

        env.step(next_point)

        updated_scene = env.get_scene()

        selected_score = scores[best]
        selected_concept = concepts[best]

        writer.writerow([
            step,
            updated_scene["time"],
            updated_scene["ego"]["x"],
            updated_scene["ego"]["y"],
            updated_scene["ego"]["speed"],
            best,
            selected_score["safety_score"],
            selected_score["efficiency_score"],
            selected_score["total_score"],
            selected_concept["minimum_distance"]
        ])

        frames.append({
            "step": step,
            "time": updated_scene["time"],
            "ego": updated_scene["ego"],
            "traffic": updated_scene["traffic"],
            "selected_path": best,
            "trajectories": trajectories,
            "scores": scores,
            "concepts": concepts
        })

        if step % 10 == 0:
            print(
                f"STEP {step} | "
                f"선택 경로: {best} | "
                f"속도: {updated_scene['ego']['speed']:.2f} | "
                f"차량 위치: {updated_scene['ego']['y']:.2f}"
            )

with open(
    json_path,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        {"frames": frames},
        file,
        ensure_ascii=False,
        indent=2
    )

print("\n===== 시뮬레이션 완료 =====")
print(f"CSV 저장: {csv_path}")
print(f"JSON 저장: {json_path}")
print(f"총 프레임: {len(frames)}")
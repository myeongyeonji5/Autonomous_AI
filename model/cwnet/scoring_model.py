
class TrajectoryScorer:
    def score(self, trajectories, concepts):
        results = {}

        for name, points in trajectories.items():
            concept = concepts[name]

            # 1. 안전성 점수
            safety_score = concept["minimum_distance"] * 2

            if concept["collision_risk"]:
                safety_score -= 100

            if concept["close_object"]:
                safety_score -= 20

            if concept["pedestrian_conflict"]:
                safety_score -= 35

            if concept["bicycle_conflict"]:
                safety_score -= 25

            # 2. 주행 효율 점수
            progress = points[-1]["x"] - points[0]["x"]
            efficiency_score = progress * 0.5

            # 3. 최종 점수
            total_score = safety_score + efficiency_score

            results[name] = {
                "safety_score": round(safety_score, 2),
                "efficiency_score": round(efficiency_score, 2),
                "total_score": round(total_score, 2)
            }

        return results

    def select_best(self, scores):
        return max(
            scores,
            key=lambda name: scores[name]["total_score"]
        )


class ConceptClassifier:

    def __init__(self, dt=0.1):
        self.dt = dt

        # 시뮬레이션용 위험 거리 기준
        self.danger_distance = 2.5
        self.close_distance = 8.0

    def predict_object_position(self, obj, t):

        # 자동차와 자전거는 일정한 속도로 이동한다고 가정
        if obj["type"] in ["car", "bicycle"]:
            x = obj["x"] + obj["speed"] * t
            y = obj["y"]

        # 보행자는 현재 방향으로 이동한다고 가정
        else:
            x = obj["x"]
            y = (
                obj["y"]
                + obj["speed"] * obj["direction"] * t
            )

        return x, y

    def classify(self, trajectories, traffic):

        results = {}

        for name, points in trajectories.items():

            min_distance = float("inf")
            nearest_type = None

            pedestrian_distance = float("inf")
            bicycle_distance = float("inf")

            # 후보 경로의 모든 지점을 검사
            for i, point in enumerate(points):

                t = i * self.dt

                for obj in traffic:

                    obj_x, obj_y = (
                        self.predict_object_position(obj, t)
                    )

                    dx = point["x"] - obj_x
                    dy = point["y"] - obj_y

                    distance = (dx**2 + dy**2) ** 0.5

                    if distance < min_distance:
                        min_distance = distance
                        nearest_type = obj["type"]

                    if obj["type"] == "pedestrian":
                        pedestrian_distance = min(
                            pedestrian_distance,
                            distance
                        )

                    elif obj["type"] == "bicycle":
                        bicycle_distance = min(
                            bicycle_distance,
                            distance
                        )

            results[name] = {
                "nearest_object": nearest_type,
                "minimum_distance": round(min_distance, 2),

                "collision_risk": int(
                    min_distance < self.danger_distance
                ),

                "close_object": int(
                    min_distance < self.close_distance
                ),

                "pedestrian_conflict": int(
                    pedestrian_distance < self.close_distance
                ),

                "bicycle_conflict": int(
                    bicycle_distance < self.close_distance
                )
            }

        return results

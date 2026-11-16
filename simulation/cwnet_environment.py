import numpy as np


class CWNetEnvironment:
    def __init__(self):
        self.dt = 0.1
        self.lane_width = 3.5
        self.lane_centers = [-1.75, 1.75]

        # 차량의 차체 폭을 고려한 안전 주행 범위
        # 중앙 노란색 선과 도로 바깥 경계에 차체가 닿지 않도록 제한
        self.vehicle_half_width = 0.9
        self.line_margin = 0.2

        self.max_acceleration = 2.5
        self.max_deceleration = 4.0
        self.max_lateral_speed = 2.0

        self.reset(seed=42)

    def reset(self, seed=None):
        self.rng = np.random.default_rng(seed)

        self.time = 0.0

        self.ego = {
            "x": 0.0,
            "y": -1.75,
            "speed": 12.0
        }

        self.traffic = [
            {
                "id": "car_1",
                "type": "car",
                "x": 40.0,
                "y": -1.75,
                "speed": 8.0
            },
            {
                "id": "car_2",
                "type": "car",
                "x": 25.0,
                "y": 1.75,
                "speed": 10.0
            },
            {
                "id": "bicycle",
                "type": "bicycle",
                "x": 30.0,
                "y": -1.75,
                "speed": 5.0
            },
            {
                "id": "pedestrian",
                "type": "pedestrian",
                "x": 60.0,
                "y": 1.75,
                "speed": 1.0,
                "direction": -1
            }
        ]

        return self.get_scene()

    def get_lane_side(self, y=None):
        if y is None:
            y = self.ego["y"]

        return -1 if y < 0 else 1

    def get_safe_lane_bounds(self, side=None):
        if side is None:
            side = self.get_lane_side()

        margin = self.vehicle_half_width + self.line_margin

        if side < 0:
            return -self.lane_width + margin, -margin

        return margin, self.lane_width - margin

    def clamp_to_current_lane(self, y):
        side = self.get_lane_side()
        min_y, max_y = self.get_safe_lane_bounds(side)

        return float(np.clip(y, min_y, max_y))

    def update_speed(self, target_speed):
        current_speed = self.ego["speed"]
        target_speed = max(0.0, float(target_speed))

        difference = target_speed - current_speed

        if difference > 0:
            change = min(
                difference,
                self.max_acceleration * self.dt
            )
        else:
            change = max(
                difference,
                -self.max_deceleration * self.dt
            )

        self.ego["speed"] = max(0.0, current_speed + change)

    def update_lateral_position(self, target_y):
        # 현재 주행 차선의 안전 범위를 절대 벗어나지 않음
        target_y = self.clamp_to_current_lane(target_y)

        current_y = self.ego["y"]
        difference = target_y - current_y

        max_change = self.max_lateral_speed * self.dt

        change = float(np.clip(
            difference,
            -max_change,
            max_change
        ))

        new_y = current_y + change

        # 매 순간 중앙선 침범 방지
        self.ego["y"] = self.clamp_to_current_lane(new_y)

    def update_traffic(self):
        for obj in self.traffic:
            if obj["type"] == "pedestrian":
                direction = obj.get("direction", 1)

                obj["y"] += (
                    obj["speed"] *
                    direction *
                    self.dt
                )

                # 보행자는 설정된 보행 구역 안에서 이동
                if obj["y"] >= 2.2:
                    obj["y"] = 2.2
                    obj["direction"] = -1

                elif obj["y"] <= -2.2:
                    obj["y"] = -2.2
                    obj["direction"] = 1

            else:
                obj["x"] += obj["speed"] * self.dt

    def step(self, selected_point=None):
        self.time += self.dt

        old_speed = self.ego["speed"]

        if selected_point is not None:
            target_speed = selected_point.get(
                "speed",
                self.ego["speed"]
            )

            target_y = selected_point.get(
                "y",
                self.ego["y"]
            )
        else:
            target_speed = self.ego["speed"]
            target_y = self.ego["y"]

        # 속도와 횡방향 위치 업데이트
        self.update_speed(target_speed)
        self.update_lateral_position(target_y)

        # 평균 속도를 사용해 전진 거리 계산
        average_speed = (
            old_speed + self.ego["speed"]
        ) / 2.0

        self.ego["x"] += average_speed * self.dt

        # 주변 객체 업데이트
        self.update_traffic()

        return self.get_scene()

    def get_scene(self):
        return {
            "time": float(self.time),
            "ego": self.ego.copy(),
            "traffic": [
                obj.copy()
                for obj in self.traffic
            ]
        }
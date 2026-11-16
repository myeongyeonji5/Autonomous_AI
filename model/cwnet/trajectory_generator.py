import numpy as np


class TrajectoryGenerator:
    def __init__(self):
        self.dt = 0.1
        self.horizon = 3.0

        self.lane_width = 3.5
        self.vehicle_half_width = 0.9
        self.line_margin = 0.2

    def get_safe_bounds(self, y):
        margin = self.vehicle_half_width + self.line_margin

        if y < 0:
            return -self.lane_width + margin, -margin

        return margin, self.lane_width - margin

    def generate(self, ego):
        v0 = max(0.0, float(ego["speed"]))
        x0 = float(ego["x"])
        y0 = float(ego["y"])

        times = np.arange(
            0,
            self.horizon + self.dt / 2,
            self.dt
        )

        min_y, max_y = self.get_safe_bounds(y0)
        safe_y = float(np.clip(y0, min_y, max_y))

        # 1. 속도 유지
        keep_speed = [
            {
                "x": x0 + v0 * t,
                "y": safe_y,
                "speed": v0
            }
            for t in times
        ]

        # 2. 감속
        deceleration = 2.0
        target_speed = max(0.0, v0 - 3.0)

        if v0 > target_speed:
            decel_time = (v0 - target_speed) / deceleration
        else:
            decel_time = 0.0

        slow_down = []

        for t in times:
            active_time = min(t, decel_time)

            current_speed = max(
                target_speed,
                v0 - deceleration * t
            )

            distance = (
                v0 * active_time
                - 0.5 * deceleration * active_time ** 2
                + target_speed * max(0.0, t - decel_time)
            )

            slow_down.append({
                "x": x0 + max(0.0, distance),
                "y": safe_y,
                "speed": current_speed
            })

        # 3. 현재 차선 안에서 바깥쪽으로 회피
        if y0 < 0:
            target_y = min_y
        else:
            target_y = max_y

        avoid_path = []

        for t in times:
            progress = min(t / 1.5, 1.0)

            smooth = (
                3 * progress ** 2
                - 2 * progress ** 3
            )

            new_y = y0 + (target_y - y0) * smooth
            new_y = float(np.clip(new_y, min_y, max_y))

            avoid_path.append({
                "x": x0 + v0 * t,
                "y": new_y,
                "speed": max(v0 - 1.0, 0.0)
            })

        # 4. 비상 정지
        stop_path = []
        emergency_deceleration = 4.0

        for t in times:
            active_time = min(
                t,
                v0 / emergency_deceleration
                if emergency_deceleration > 0 else 0.0
            )

            current_speed = max(
                0.0,
                v0 - emergency_deceleration * t
            )

            distance = (
                v0 * active_time
                - 0.5 * emergency_deceleration * active_time ** 2
            )

            stop_path.append({
                "x": x0 + max(0.0, distance),
                "y": safe_y,
                "speed": current_speed
            })

        return {
            "keep_speed": keep_speed,
            "slow_down": slow_down,
            "change_lane": avoid_path,
            "stop": stop_path
        }
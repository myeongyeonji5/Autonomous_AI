
import gymnasium as gym
from gymnasium import spaces
import numpy as np


class DrivingEnvironment(gym.Env):

    def __init__(self):
        super().__init__()

        self.action_space = spaces.Discrete(3)

        # 정규화된 상태 공간
        self.observation_space = spaces.Box(
            low=np.array([0, 0, -1], dtype=np.float32),
            high=np.array([1, 1, 1], dtype=np.float32),
            dtype=np.float32
        )

        self.dt = 0.1
        self.max_steps = 500
        self.step_count = 0

        self.reset()

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.distance = float(self.np_random.uniform(70, 100))
        self.speed = 20.0
        self.obstacle_speed = float(
            self.np_random.uniform(0, 15)
        )

        self.relative_speed = self.speed - self.obstacle_speed
        self.step_count = 0

        return self._get_state(), {}

    def _get_state(self):

        return np.array([
            self.distance / 100.0,
            self.speed / 30.0,
            self.relative_speed / 30.0
        ], dtype=np.float32)

    def step(self, action):

        self.step_count += 1

        # 차량 행동
        if action == 0:
            self.speed = min(self.speed + 1, 30)

        elif action == 1:
            self.speed = max(self.speed - 2, 0)

        elif action == 2:
            self.speed = 0

        # 장애물 속도 변화
        self.obstacle_speed = np.clip(
            self.obstacle_speed
            + self.np_random.uniform(-0.5, 0.5),
            0,
            15
        )

        # 상대 속도 계산
        self.relative_speed = (
            self.speed - self.obstacle_speed
        )

        # 거리 변화
        self.distance -= self.relative_speed * self.dt

        # 기본 보상
        reward = 0.1

        terminated = False
        truncated = False

        # 충돌
        if self.distance <= 0:
            reward = -100.0
            terminated = True

        # 위험 거리
        elif self.distance < 10:
            reward = -5.0

        elif self.distance < 20:
            reward = -2.0

        # 주행 효율
        elif self.speed > 0:
            reward = 0.2

        # 불필요한 정지
        if action == 2 and self.distance > 20:
            reward -= 0.2

        # 최대 시간 제한
        if self.step_count >= self.max_steps:
            truncated = True

        return (
            self._get_state(),
            reward,
            terminated,
            truncated,
            {}
        )

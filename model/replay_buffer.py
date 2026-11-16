
import random
from collections import deque


class ReplayBuffer:

    def __init__(self, capacity=10000):
        # 최대 저장 가능한 경험 개수
        self.buffer = deque(maxlen=capacity)

    def add(self, state, action, reward, next_state, done):
        # 하나의 경험 저장
        experience = (
            state,
            action,
            reward,
            next_state,
            done
        )

        self.buffer.append(experience)

    def sample(self, batch_size):
        # 저장된 경험 중 무작위 추출
        batch = random.sample(self.buffer, batch_size)

        states, actions, rewards, next_states, dones = zip(*batch)

        return (
            states,
            actions,
            rewards,
            next_states,
            dones
        )

    def __len__(self):
        return len(self.buffer)

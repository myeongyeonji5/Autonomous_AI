
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

from model.dqn import DQN
from model.replay_buffer import ReplayBuffer


class DQNAgent:

    def __init__(self):
        # 실행 장치
        self.device = torch.device("cpu")

        # 신경망 생성
        self.policy_net = DQN().to(self.device)
        self.target_net = DQN().to(self.device)

        # 타깃 네트워크 초기화
        self.target_net.load_state_dict(
            self.policy_net.state_dict()
        )

        self.target_net.eval()

        # 학습 설정
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.995

        self.batch_size = 64
        self.learning_rate = 0.001

        # 최적화 함수
        self.optimizer = optim.Adam(
            self.policy_net.parameters(),
            lr=self.learning_rate
        )

        self.loss_function = nn.SmoothL1Loss()

        # 경험 재생 버퍼
        self.memory = ReplayBuffer(capacity=10000)

        # 학습 횟수
        self.learn_steps = 0

    # 행동 선택
    def select_action(self, state):

        if random.random() < self.epsilon:
            return random.randrange(3)

        state_tensor = torch.tensor(
            state,
            dtype=torch.float32,
            device=self.device
        )

        with torch.no_grad():
            q_values = self.policy_net(state_tensor)

        return torch.argmax(q_values).item()

    # 경험 저장
    def remember(self, state, action, reward, next_state, done):

        self.memory.add(
            state,
            action,
            reward,
            next_state,
            done
        )

    # 신경망 학습
    def learn(self):

        if len(self.memory) < self.batch_size:
            return None

        # 경험 무작위 추출
        states, actions, rewards, next_states, dones = (
            self.memory.sample(self.batch_size)
        )

        # 텐서 변환
        states = torch.tensor(
            np.array(states), dtype=torch.float32
        )

        actions = torch.tensor(
            actions, dtype=torch.long
        ).unsqueeze(1)

        rewards = torch.tensor(
            rewards, dtype=torch.float32
        )

        next_states = torch.tensor(
            np.array(next_states), dtype=torch.float32
        )

        dones = torch.tensor(
            dones, dtype=torch.float32
        )

        # 현재 행동의 Q값
        current_q = self.policy_net(states).gather(
            1, actions
        ).squeeze(1)

        # 다음 상태의 최대 Q값
        with torch.no_grad():
            next_q = self.target_net(next_states).max(
                dim=1
            )[0]

            target_q = rewards + self.gamma * next_q * (1 - dones)

        # 손실 계산
        loss = self.loss_function(current_q, target_q)

        # 역전파 및 가중치 업데이트
        self.optimizer.zero_grad()
        loss.backward()

        # 기울기 제한
        nn.utils.clip_grad_norm_(
            self.policy_net.parameters(), 10.0
        )

        self.optimizer.step()

        # 탐험 비율 감소
        self.epsilon = max(
            self.epsilon_min,
            self.epsilon * self.epsilon_decay
        )

        # 타깃 네트워크 업데이트
        self.learn_steps += 1

        if self.learn_steps % 100 == 0:
            self.target_net.load_state_dict(
                self.policy_net.state_dict()
            )

        return loss.item()

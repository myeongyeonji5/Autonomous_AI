print("TRAIN.PY 실행 확인")

import sys
import os
import torch
import numpy as np
import pandas as pd

from simulation.environment import DrivingEnvironment
from model.agent import DQNAgent


def train():

    env = DrivingEnvironment()
    agent = DQNAgent()

    episodes = 1000

    results = []

    print("===== DQN 자율주행 AI 학습 시작 =====")

    for episode in range(1, episodes + 1):

        state, _ = env.reset()

        total_reward = 0
        total_loss = []
        done = False

        while not done:

            action = agent.select_action(state)

            next_state, reward, terminated, truncated, _ = (
                env.step(action)
            )

            done = terminated or truncated

            agent.remember(
                state,
                action,
                reward,
                next_state,
                terminated
            )

            loss = agent.learn()

            if loss is not None:
                total_loss.append(loss)

            state = next_state
            total_reward += reward

        avg_loss = (
            np.mean(total_loss)
            if total_loss else 0
        )

        results.append({
            "episode": episode,
            "reward": total_reward,
            "loss": avg_loss,
            "epsilon": agent.epsilon
        })

        if episode % 10 == 0:
            print(
                f"Episode: {episode}/{episodes} | "
                f"Reward: {total_reward:.2f} | "
                f"Loss: {avg_loss:.4f} | "
                f"Epsilon: {agent.epsilon:.3f}"
            )

    # 결과 저장
    os.makedirs("results", exist_ok=True)

    df = pd.DataFrame(results)

    df.to_csv(
        "results/training_results.csv",
        index=False
    )

    # 모델 저장
    torch.save(
        agent.policy_net.state_dict(),
        "results/dqn_model.pth"
    )

    print("\n===== 학습 완료 =====")
    print("학습 결과: results/training_results.csv")
    print("학습 모델: results/dqn_model.pth")


if __name__ == "__main__":
    print("학습 함수 호출")
    train()

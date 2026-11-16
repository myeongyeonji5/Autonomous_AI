
import torch
import torch.nn as nn


class DQN(nn.Module):

    def __init__(self, input_size=3, hidden_size=64, output_size=3):
        super(DQN, self).__init__()

        # 신경망 구조
        self.network = nn.Sequential(

            # 입력층 → 첫 번째 은닉층
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),

            # 첫 번째 은닉층 → 두 번째 은닉층
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),

            # 두 번째 은닉층 → 출력층
            nn.Linear(hidden_size, output_size)
        )

    def forward(self, state):
        return self.network(state)

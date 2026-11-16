
from simulation.cwnet_environment import CWNetEnvironment

env = CWNetEnvironment()

scene = env.reset(seed=42)

print("===== 초기 도로 상황 =====")
print(scene)

print("\n===== 5초 후 도로 상황 =====")

for _ in range(50):
    scene = env.step()

print(scene)

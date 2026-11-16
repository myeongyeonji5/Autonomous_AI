
from simulation.cwnet_environment import CWNetEnvironment
from model.cwnet.trajectory_generator import TrajectoryGenerator

env = CWNetEnvironment()

scene = env.reset(seed=42)

generator = TrajectoryGenerator()

trajectories = generator.generate(scene["ego"])

for name, points in trajectories.items():

    print(f"\n===== {name} =====")

    print("시작 위치:", points[0])
    print("중간 위치:", points[15])
    print("최종 위치:", points[-1])

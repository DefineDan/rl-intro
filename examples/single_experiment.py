import matplotlib.pyplot as plt
from dataclasses import asdict
from pathlib import Path
import json

from rl_intro.agent.core import AgentConfig
from rl_intro.agent.agent_expected_sarsa import AgentExpectedSarsa
from rl_intro.environment.gridworld import GridWorld, GridWorldConfig
from rl_intro.agent.policy import EpsilonGreedyPolicy, EpsilonGreedyConfig
from rl_intro.simulation.experiment import Experiment, ExperimentConfig
from rl_intro.evaluation.parse import parse_experiment_json
from rl_intro.evaluation.analyze import analyze_experiment
from rl_intro.evaluation.plot import (
    plot_state_visit_frequency,
    plot_final_values,
    plot_cumulative_reward,
    plot_average_reward_per_episode,
)
from rl_intro.utils.logger import logger

# from rl_intro.utils.visualize import grid_str

# ! configurations: change these as needed

out_dir = Path(__file__).parent.parent / "data"

n_rows, n_cols = 4, 10
n_actions = 4

env_config = GridWorldConfig(
    width=n_cols,
    height=n_rows,
    start_states=[0],
    terminal_states=[39],
    cliff_states=[4, 24, 5, 25],
    wall_states=[2, 12, 22, 17, 27, 37],
    random_seed=42,
)

agent_config = AgentConfig(
    n_states=n_cols * n_rows,
    n_actions=n_actions,
    random_seed=42,
    learning_rate=0.3,
    discount=1.0,
)

policy_config = EpsilonGreedyConfig(epsilon=0.1)

experiment_config = ExperimentConfig(n_episodes=1000, max_steps=200)


def run_experiment(log_file: Path):
    agent = AgentExpectedSarsa(agent_config, EpsilonGreedyPolicy(policy_config))
    env = GridWorld(env_config)
    experiment = Experiment(agent, env, experiment_config)

    logger.info(f"Environment: {env.to_str()}")
    logger.info(f"Agent: {agent}")

    # * running the experiment
    experiment_log = experiment.run()

    # * log extra information like this
    # logger.debug(agent.policy.get_distribution(agent))
    # logger.debug(grid_str(agent.get_greedy_actions(), n_cols, n_rows))
    # logger.debug(grid_str(agent.get_greedy_values(), n_cols, n_rows))

    with open(log_file, "w") as f:
        json.dump(asdict(experiment_log), f, indent=4)
    logger.info(f"Experiment completed and logs saved to '{log_file}'.")


def analyze(log_file: Path):
    assert log_file.exists(), f"Log file {log_file} does not exist."

    experiment_log = parse_experiment_json(log_file)
    experiment_analysis = analyze_experiment(experiment_log, n_rows, n_cols)

    fig, ax = plt.subplots(2, 2, figsize=(12, 10))
    ax = ax.flatten()
    plot_cumulative_reward([experiment_analysis], ax[0], interval=(0, 20000))
    plot_average_reward_per_episode([experiment_analysis], ax[1], interval=(0, 300))
    plot_final_values(experiment_analysis, ax[2])
    plot_state_visit_frequency(experiment_analysis, ax[3])
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    logger.setLevel("INFO")
    out_dir.mkdir(parents=True, exist_ok=True)
    save_path = out_dir / "single_experiment_logs.json"

    run_experiment(save_path)
    analyze(save_path)

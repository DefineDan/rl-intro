import matplotlib.pyplot as plt
from dataclasses import asdict
from pathlib import Path
import json

from rl_intro.agent.core import AgentConfig
from rl_intro.agent.agent_expected_sarsa import AgentExpectedSarsa
from rl_intro.agent.agent_sarsa import AgentSarsa
from rl_intro.agent.agent_q_learning import AgentQLearning
from rl_intro.environment.gridworld import GridWorld, GridWorldConfig
from rl_intro.agent.policy import EpsilonGreedyPolicy, EpsilonGreedyConfig
from rl_intro.simulation.experiment import (
    ExperimentBatch,
    ExperimentConfig,
    AgentRecipe,
    EnvironmentRecipe,
)
from rl_intro.evaluation.parse import parse_experiment_batch_json
from rl_intro.evaluation.analyze import analyze_experiments
from rl_intro.evaluation.plot import (
    plot_state_visit_frequency,
    plot_final_values,
    plot_cumulative_reward,
    plot_average_reward_per_episode,
)
from rl_intro.utils.logger import logger

# * configurations: change these as needed

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

environment_recipe = EnvironmentRecipe(
    environment_class=GridWorld,
    environment_config=env_config,
)

agent_config = AgentConfig(
    n_states=n_cols * n_rows,
    n_actions=n_actions,
    random_seed=42,
    learning_rate=0.3,
    discount=1.0,
)
policy_config = EpsilonGreedyConfig(epsilon=0.1)

agent_sarsa_recipe = AgentRecipe(
    agent_class=AgentSarsa,
    agent_config=agent_config,
    policy_class=EpsilonGreedyPolicy,
    policy_config=policy_config,
)

agent_expected_sarsa_recipe = AgentRecipe(
    agent_class=AgentExpectedSarsa,
    agent_config=agent_config,
    policy_class=EpsilonGreedyPolicy,
    policy_config=policy_config,
)

agent_q_learning_recipe = AgentRecipe(
    agent_class=AgentQLearning,
    agent_config=agent_config,
    policy_class=EpsilonGreedyPolicy,
    policy_config=policy_config,
)

experiment_config = ExperimentConfig(n_episodes=1000, max_steps=200)


def run_experiment(log_file: Path):
    experiment_batch = ExperimentBatch(
        agent_recipes=[
            agent_sarsa_recipe,
            agent_expected_sarsa_recipe,
            agent_q_learning_recipe,
        ],
        env_recipes=[environment_recipe],
        experiment_config=experiment_config,
        n_runs=10,
    )

    # * running the experiment
    experiment_logs = experiment_batch.run()

    with open(log_file, "w") as f:
        json.dump([asdict(log) for log in experiment_logs], f, indent=4)
    logger.info(f"Experiment completed and logs saved to '{log_file}'.")


def analyze(log_file: Path):
    assert log_file.exists(), f"Log file {log_file} does not exist."

    experiment_logs = parse_experiment_batch_json(log_file)
    experiment_results = analyze_experiments(
        experiment_logs, n_rows, n_cols, agent_grouping=True
    )

    n_results = len(experiment_results)  # seeds for each agent are grouped together
    logger.info(f"Grouped analysis into {n_results} result(s)")

    fig, ax = plt.subplots(1 + n_results, 2, figsize=(12, max(n_results * 4, 8)))
    ax = ax.flatten()
    plot_cumulative_reward(experiment_results, ax[0], interval=(0, 20000))
    plot_average_reward_per_episode(experiment_results, ax[1], interval=(0, -1))
    for i, experiment_analysis in enumerate(experiment_results):
        plot_final_values(experiment_analysis, ax[2 + i * 2])
        plot_state_visit_frequency(experiment_analysis, ax[3 + i * 2])
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    logger.setLevel("INFO")
    out_dir.mkdir(parents=True, exist_ok=True)
    save_path = out_dir / "single_experiment_logs.json"

    run_experiment(save_path)
    analyze(save_path)

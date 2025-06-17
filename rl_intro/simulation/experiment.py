from rl_intro.agent.core import Agent
from rl_intro.environment.core import Environment
from rl_intro.environment.core import State, Action, Reward, Terminal
from dataclasses import dataclass
from typing import Optional
from tqdm import trange
import json
from rl_intro.utils.logger import logger
from rl_intro.utils.visualize import grid_str


@dataclass
class ExperimentLog:
    episode: int
    step: int
    action: Action
    state: State
    reward: Reward
    terminal: Terminal


@dataclass
class ExperimentConfig:
    n_episodes: int = 1000
    max_steps: int = 100


class Experiment:
    def __init__(self, agent: Agent, env: Environment, config: ExperimentConfig):
        self.agent = agent
        self.env = env
        self.config = config

    def run_episodes(self, n_episodes: int, max_steps: int) -> list[ExperimentLog]:
        logs = []
        for episode in trange(n_episodes, desc="Episodes"):
            self.env.reset()
            action = self.agent.start(self.env.state)
            for step in range(1, max_steps + 1):
                state, reward, terminal = self.env.step(action)
                logs.append(
                    ExperimentLog(
                        episode=episode,
                        step=step,
                        action=Action(action),
                        state=State(state),
                        reward=Reward(reward),
                        terminal=Terminal(terminal),
                    )
                )
                action = self.agent.step(state, reward, terminal)
                if terminal:
                    break
            else:
                logger.warning(
                    f"Agent took too many steps ({self.config.max_steps}) in episode {episode}, resetting."
                )
        return logs

    def run(self) -> list[ExperimentLog]:
        return self.run_episodes(self.config.n_episodes, self.config.max_steps)


if __name__ == "__main__":
    # Example usage
    from rl_intro.agent.agent_sarsa import AgentSarsa, AgentSarsaConfig
    from rl_intro.environment.gridworld import GridWorld, GridWorldConfig
    from rl_intro.agent.policy import EpsilonGreedyPolicy, EpsilonGreedyConfig

    w, h = 10, 4

    env_config = GridWorldConfig(
        width=w,
        height=h,
        start_states=[0],
        terminal_states=[9],
        cliff_states=[1, 2, 3, 4, 5, 6, 7, 8],
        wall_states=[],
        random_seed=42,
    )
    env = GridWorld(env_config)

    agent_config = AgentSarsaConfig(
        n_states=w * h,
        n_actions=len(env.action_space),
        random_seed=42,
        learning_rate=0.3,
        discount=1.0,
    )
    agent = AgentSarsa(
        agent_config, EpsilonGreedyPolicy(EpsilonGreedyConfig(epsilon=0.1))
    )
    experiment_config = ExperimentConfig(n_episodes=2000, max_steps=200)
    experiment = Experiment(agent, env, experiment_config)

    logger.info(f"Agent: {agent}")
    logger.debug(env.to_str())
    logger.debug(agent.policy.get_distribution(agent))
    logger.debug(grid_str(agent.get_greedy_values(), w, h))

    # ! running the experiment
    logs = experiment.run()

    logger.debug(agent.policy.get_distribution(agent))
    logger.debug(grid_str(agent.get_greedy_actions(), w, h))
    logger.debug(grid_str(agent.get_greedy_values(), w, h))
    logger.debug(env.to_str())

    # save the logs as a json file
    with open("experiment_logs.json", "w") as f:
        json.dump([log.__dict__ for log in logs], f, indent=4)
    logger.info("Experiment completed and logs saved to 'experiment_logs.json'.")

from rl_intro.agent.core import Agent
from rl_intro.environment.core import Environment
from rl_intro.environment.core import State, Action, Reward, Terminal
from dataclasses import dataclass
from typing import Optional
from tqdm import trange
import json


@dataclass
class ExperimentLog:
    episode: int
    step: int
    state: State
    action: Action
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
        self.episodes = 0
        self.steps = 0
        self.last_action: Action = self.start_episode()

    def start_episode(self) -> Action:
        self.env.reset()
        self.last_action = self.agent.start(self.env.state)
        return self.last_action

    def step(self) -> ExperimentLog:
        self.steps += 1
        state, reward, terminal = self.env.step(self.last_action)
        action = self.agent.step(state, reward, terminal)
        self.last_action = action
        log = ExperimentLog(
            episode=self.episodes,
            step=self.steps,
            state=State(state),
            action=Action(action),
            reward=Reward(reward),
            terminal=Terminal(terminal),
        )
        if terminal:
            print(
                f"JUHU, reached terminal with reward {reward} in episode {self.episodes} at step {self.steps}."
            )
            self.episodes += 1
            self.steps = 0
            self.start_episode()

        if self.steps > self.config.max_steps:
            raise ValueError("Agent took too many steps, please check")
        return log

    def run(self) -> list[ExperimentLog]:
        logs = []
        for _ in trange(self.config.n_episodes, desc="Episodes"):
            log = self.step()
            logs.append(log)
        return logs


if __name__ == "__main__":
    # Example usage
    from rl_intro.agent.agent_sarsa import AgentSarsa, AgentSarsaConfig
    from rl_intro.environment.gridworld import GridWorld, GridWorldConfig
    from rl_intro.agent.policy import EpsilonGreedyPolicy, EpsilonGreedyConfig

    env_config = GridWorldConfig(
        width=5,
        height=5,
        start_states=[1],
        terminal_states=[24],
        cliff_states=[20, 21],
        wall_states=[6, 7, 8, 9],
        random_seed=42,
    )
    env = GridWorld(env_config)
    env.print()

    agent_config = AgentSarsaConfig(
        n_states=env_config.width * env_config.height,
        n_actions=4,
        random_seed=42,
        learning_rate=0.1,
        discount=0.9,
    )
    agent = AgentSarsa(
        agent_config, EpsilonGreedyPolicy(EpsilonGreedyConfig(epsilon=0.1))
    )
    experiment_config = ExperimentConfig(n_episodes=5000, max_steps=200)
    experiment = Experiment(agent, env, experiment_config)
    logs = experiment.run()
    # save the logs as a json file

    with open("experiment_logs.json", "w") as f:
        json.dump([log.__dict__ for log in logs], f, indent=4)
    print("Experiment completed and logs saved to 'experiment_logs.json'.")

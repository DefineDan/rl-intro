from dataclasses import dataclass
from typing import List, Optional
import numpy as np
import random
from rl_intro.agent.core import Agent, AgentConfig, Policy, PolicyConfig
from rl_intro.environment.core import Reward, State, Action, Terminal


class RandomPolicy(Policy):

    def __init__(self, config: PolicyConfig):
        self.config = config

    def select_action(self, agent: Agent, state: State, reward: Reward) -> Action:
        return agent.random_generator.choice(agent.config.action_space)


@dataclass
class EpsilonGreedyConfig(PolicyConfig):
    epsilon: float = 0.1


class EpsilonGreedyPolicy(Policy):
    def __init__(self, config: EpsilonGreedyConfig):
        self.config = config
        self.x = 5

    def select_action(self, agent: Agent, state: State, reward: Reward) -> Action:
        if agent.random_generator.random() < self.config.epsilon:  # TODO use agent rand
            # Explore: random action
            return agent.random_generator.choice(agent.config.action_space)
        else:
            # Exploit: best action from Q-table
            state_idx = agent.config.state_space.index(state)
            q_values = agent.q[state_idx]
            max_q = np.max(q_values)
            best_actions = [
                a for a, q in zip(agent.config.action_space, q_values) if q == max_q
            ]
            return random.choice(best_actions)

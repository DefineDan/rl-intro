from dataclasses import dataclass
from typing import List, Optional
import numpy as np
import random
from rl_intro.agent.core import Agent, AgentConfig, Policy, PolicyConfig
from rl_intro.environment.core import Reward, State, Action, Terminal
from rl_intro.utils.math import fair_argmax


class RandomPolicy(Policy):
    def select_action(
        self, agent: Agent, state: State, reward: Optional[Reward]
    ) -> Action:
        return agent.random_generator.choice(agent.config.n_actions)


@dataclass
class EpsilonGreedyConfig(PolicyConfig):
    epsilon: float = 0.1


class EpsilonGreedyPolicy(Policy):
    def __init__(self, config: EpsilonGreedyConfig):
        self.config = config

    def select_action(
        self, agent: Agent, state: State, reward: Optional[Reward]
    ) -> Action:
        if agent.random_generator.random() < self.config.epsilon:
            # Explore: random action
            return agent.random_generator.choice(agent.config.n_actions)
            # Exploit: best action from Q-table
        else:
            q_values = agent.q[state]
            action, value = fair_argmax(q_values, agent.random_generator)
            return action

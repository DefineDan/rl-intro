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

    def get_distribution(self, agent: Agent) -> np.ndarray:
        return np.full(
            (agent.config.n_states, agent.config.n_actions),
            1.0 / agent.config.n_actions,
        )

    def get_state_distribution(self, agent: Agent, state: State) -> np.ndarray:
        return np.full(agent.config.n_actions, 1.0 / agent.config.n_actions)


@dataclass
class EpsilonGreedyConfig(PolicyConfig):
    epsilon: float = 0.1


class EpsilonGreedyPolicy(Policy):
    def __init__(self, config: EpsilonGreedyConfig):
        self.config = config

    def __str__(self):
        return f"EpsilonGreedyPolicy(epsilon={self.config.epsilon})"

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

    def get_distribution(self, agent: Agent) -> np.ndarray:
        n_states = agent.config.n_states
        n_actions = agent.config.n_actions
        distribution = np.full((n_states, n_actions), self.config.epsilon / n_actions)

        # Fairly distribute the (1 - epsilon) probability among all best actions
        for s in range(n_states):
            max_q = np.max(agent.q[s])
            best_actions = np.flatnonzero(agent.q[s] == max_q)
            distribution[s, best_actions] += (1 - self.config.epsilon) / len(
                best_actions
            )
        return distribution

    def get_state_distribution(self, agent: Agent, state: State) -> np.ndarray:
        n_actions = agent.config.n_actions
        distribution = np.full(n_actions, self.config.epsilon / n_actions)

        max_q = np.max(agent.q[state])
        best_actions = np.flatnonzero(agent.q[state] == max_q)
        distribution[best_actions] += (1 - self.config.epsilon) / len(best_actions)

        return distribution

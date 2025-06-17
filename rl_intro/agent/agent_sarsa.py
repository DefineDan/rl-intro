from rl_intro.agent.core import Agent, AgentConfig, Policy, PolicyConfig
from rl_intro.environment.core import Reward, Action, Terminal, State
from dataclasses import dataclass
from typing import List, Optional, Protocol
import numpy as np
import random
from rl_intro.utils.math import fair_argmax
from numpy.typing import NDArray
from rl_intro.utils.logger import logger

# TODO: fix action space indexing


@dataclass
class AgentSarsaConfig(AgentConfig):
    learning_rate: float = 0.1
    discount: float = 1.0


class AgentSarsa(Agent):
    def __init__(self, config: AgentSarsaConfig, policy: Policy):
        self.config = config
        self.policy = policy

        self.last_state: Optional[State] = None
        self.last_action: Optional[Action] = None

        self.q = np.zeros((self.config.n_states, self.config.n_actions))
        self.random_generator = np.random.default_rng(config.random_seed)

        logger.debug(f"AgentSarsa with random seed {config.random_seed} initialized.")

    def __str__(self):
        return f"SarsaAgent(seed={self.config.random_seed},learning_rate={self.config.learning_rate},discount={self.config.discount},policy={self.policy})"

    def start(self, state: State) -> Action:
        action = self.policy.select_action(self, state, None)
        self.last_state = state
        self.last_action = action
        return action

    def step(self, state: State, reward: Reward, terminal: Terminal) -> Action:
        action = self.policy.select_action(self, state, reward)
        self.learn(state, reward, terminal, action)
        self.last_state = state
        self.last_action = action
        return action

    def learn(
        self, state: State, reward: Reward, terminal: Terminal, action: Action
    ) -> None:
        if terminal:
            td_error = reward - self.q[self.last_state, self.last_action]
        else:
            td_error = (
                reward
                + self.config.discount * self.q[state, action]
                - self.q[self.last_state, self.last_action]
            )
        self.q[self.last_state, self.last_action] += (
            self.config.learning_rate * td_error
        )

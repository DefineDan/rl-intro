from rl_intro.agent.core import Agent, AgentConfig, Policy, PolicyConfig
from rl_intro.environment.core import Reward, Action, Terminal, State
from dataclasses import dataclass
from typing import List, Optional, Protocol
import numpy as np
import random


@dataclass
class QAgentConfig(AgentConfig):
    alpha: float = 0.1
    gamma: float = 0.9


class QLearningAgent(Agent):
    def __init__(self, config: QAgentConfig, policy: Policy):
        self.config = config
        self.policy = policy
        self.last_reward: Optional[Reward] = None
        self.last_state: Optional[State] = None
        self.last_action: Optional[Action] = None
        self.q = np.zeros((config.n_states, config.n_actions))
        self.random_generator = np.random.default_rng(config.random_seed)

    def step(self, state: State, reward: Reward, terminal: Terminal) -> Action:
        action = self.policy.select_action(self, state, reward)
        self.last_reward = reward
        self.last_state = state
        self.last_action = action
        self.config.gamma
        return action

from rl_intro.environment.core import (
    Reward,
    State,
    Terminal,
    Action,
)
from typing import Protocol
from dataclasses import dataclass
from typing import List, Optional
from numpy.typing import NDArray
from abc import ABC, abstractmethod
import numpy as np


@dataclass
class PolicyConfig:
    pass


@dataclass
class AgentConfig:
    state_space: List[State]
    action_space: List[Action]
    policy_config: PolicyConfig
    random_seed: Optional[int] = None


class Agent(ABC):
    q: NDArray
    random_generator: np.random.Generator

    def __init__(self, config: AgentConfig, policy: "Policy"):
        self.config = config
        self.policy = policy

    @abstractmethod
    def step(self, state: State, reward: Reward, terminal: Terminal) -> Action:
        pass


class Policy(ABC):
    def __init__(self, config: PolicyConfig):
        self.config = config

    @abstractmethod
    def select_action(self, agent: Agent, state: State, reward: Reward) -> Action:
        pass

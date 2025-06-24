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
    n_states: int
    n_actions: int
    learning_rate: float = 0.1
    discount: float = 1.0
    random_seed: Optional[int] = None


class Agent(ABC):
    q: NDArray
    random_generator: np.random.Generator

    def __init__(self, config: AgentConfig, policy: "Policy"):
        self.config = config
        self.policy = policy

    @abstractmethod
    def step(
        self, state: State, reward: Optional[Reward], terminal: Terminal
    ) -> Action:
        pass

    def get_greedy_actions(self) -> np.ndarray:
        return np.argmax(self.q, axis=1)

    def get_greedy_values(self) -> np.ndarray:
        return np.max(self.q, axis=1)


class Policy(ABC):
    def __init__(self, config: PolicyConfig):
        self.config = config

    @abstractmethod
    def select_action(
        self, agent: Agent, state: State, reward: Optional[Reward]
    ) -> Action:
        pass

    @abstractmethod
    def get_distribution(self, agent: Agent) -> NDArray:
        """
        Returns a (num_states, num_actions) array where each row is the action distribution for a state.
        """
        pass

    @abstractmethod
    def get_state_distribution(self, agent: Agent, state: State) -> np.ndarray:
        """
        Returns the action distribution for a specific state.
        """
        pass

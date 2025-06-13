from rl_intro.environment.environment_types import (
    Reward,
    State,
    Terminal,
    Action,
)
from typing import Protocol
from dataclasses import dataclass


class Agent(Protocol):
    def step(self, state: State, reward: Reward, terminal: Terminal) -> Action: ...
    def choose_action(self) -> Action: ...

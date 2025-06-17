from dataclasses import dataclass
from typing import Protocol
from typing import Tuple, Optional

Reward = float
State = int
Terminal = bool
Action = int


@dataclass
class EnvironmentConfig:
    random_seed: Optional[int]


class Environment(Protocol):
    state: State

    def __init__(self, config): ...
    def reset(self) -> State: ...
    def step(self, action: Action) -> Tuple[State, Reward, Terminal]: ...
    def to_str(self) -> str: ...

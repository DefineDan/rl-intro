from dataclasses import dataclass
from typing import Protocol
from typing import Tuple

Reward = float
State = int
Terminal = bool
Action = int


class Environment(Protocol):
    def reset(self) -> State: ...
    def step(self, action: Action) -> Tuple[State, Reward, Terminal]: ...

from environment_types import Environment, State, Reward, Action
from dataclasses import dataclass
from typing import Tuple, List, Optional, Literal, Callable
import numpy as np
from enum import StrEnum, Enum


class StateKind(Enum):
    EMPTY = 0
    START = 1
    TERMINAL = 2
    CLIFF = 3
    WALL = 4


@dataclass
class GridWorldConfig:
    width: int
    height: int
    start_states: List[State]
    terminal_states: List[State]
    cliff_states: List[State]
    wall_states: List[State]
    reward_function: Callable[[State, StateKind], Reward]


class GridWorld:
    def __init__(self, config: GridWorldConfig):
        self.config = config
        self._setup_grid()

    def get_state(self, position: Tuple[int, int]) -> State:
        return position[0] * self.config.width + position[1]

    def get_position(self, state: State) -> Tuple[int, int]:
        return (state // self.config.width, state % self.config.width)

    def get_kind(self, state: State) -> StateKind:
        if state in self.config.start_states:
            return StateKind.START
        elif state in self.config.terminal_states:
            return StateKind.TERMINAL
        elif state in self.config.cliff_states:
            return StateKind.CLIFF
        elif state in self.config.wall_states:
            return StateKind.WALL
        else:
            return StateKind.EMPTY

    def _setup_grid(self):
        self.grid = np.zeros((self.config.height, self.config.width), dtype=int)
        for s in range(self.config.width * self.config.height):
            kind = self.get_kind(s)
            self.grid[self.get_position(s)] = kind.value

    def plot(self):
        for row in self.grid:
            print(" ".join(StateKind(k).name[0] for k in row))


if __name__ == "__main__":
    config = GridWorldConfig(
        width=5,
        height=5,
        start_states=[1],
        terminal_states=[24],
        cliff_states=[20, 21, 22, 23],
        wall_states=[7, 8, 9],
        reward_function=lambda state, kind: -1 if kind == StateKind.CLIFF else 0,
    )

    grid_world = GridWorld(config)
    grid_world.plot()

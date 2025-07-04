from rl_intro.environment.core import (
    State,
    Reward,
    Action,
    Terminal,
    EnvironmentConfig,
)
from dataclasses import dataclass
from typing import Tuple, List, Optional, Literal, Callable
import numpy as np
from enum import StrEnum, Enum
from rl_intro.utils.logger import logger
from rl_intro.utils.visualize import grid_str


class StateKind(Enum):
    EMPTY = 0
    START = 1
    TERMINAL = 2
    CLIFF = 3
    WALL = 4


class Act(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


def default_reward_function(state: State, kind: StateKind) -> Reward:
    if kind == StateKind.CLIFF.value:
        return -100.0
    elif kind == StateKind.TERMINAL.value:
        return 1.0
    else:
        return -1.0


@dataclass
class GridWorldConfig(EnvironmentConfig):
    width: int
    height: int
    start_states: List[State]
    terminal_states: List[State]
    cliff_states: List[State]
    wall_states: List[State]
    reward_function: Callable[[State, StateKind], Reward] = default_reward_function


class GridWorld:
    def __init__(self, config: GridWorldConfig):
        self.config = config
        self.random_generator = np.random.default_rng(config.random_seed)
        self.reward_function = config.reward_function
        self.state = self.reset()
        self.grid = self._setup_grid()

    def __str__(self):
        return f"GridWorld(w={self.config.width},h={self.config.height},s={self.config.start_states},t={self.config.terminal_states},c={self.config.cliff_states},w={self.config.wall_states})"

    @property
    def width(self) -> int:
        return self.config.width

    @property
    def height(self) -> int:
        return self.config.height

    @property
    def state_space(self) -> List[State]:
        return list(range(self.config.width * self.config.height))

    @property
    def action_space(self) -> List[Action]:
        return [
            Act.UP.value,
            Act.DOWN.value,
            Act.LEFT.value,
            Act.RIGHT.value,
        ]

    @property
    def terminal(self) -> Terminal:
        return self.grid[self.get_position(self.state)] in [
            StateKind.TERMINAL.value,
            StateKind.CLIFF.value,
        ]

    @property
    def state_kind(self) -> StateKind:
        return self.grid[self.get_position(self.state)]

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
        return self.grid

    def _select_start_state(self) -> State:
        assert self.config.start_states, "No start states defined in the configuration."
        return State(self.random_generator.choice(self.config.start_states))

    def reset(self) -> State:
        self.state = self._select_start_state()
        return self.state

    def step(self, action: Action) -> Tuple[State, Reward, Terminal]:
        self.state = self._get_next_state(action)
        reward = self.reward_function(self.state, self.state_kind)
        return self.state, reward, self.terminal

    def _get_next_state(self, action: Action) -> State:
        if self.terminal:
            return self._select_start_state()
        position = self.get_position(self.state)
        new_position = None
        if action == Act.UP.value:
            new_position = (max(0, position[0] - 1), position[1])
        elif action == Act.DOWN.value:
            new_position = (min(self.height - 1, position[0] + 1), position[1])
        elif action == Act.LEFT.value:
            new_position = (position[0], max(0, position[1] - 1))
        elif action == Act.RIGHT.value:
            new_position = (position[0], min(self.width - 1, position[1] + 1))
        else:
            raise ValueError(f"Invalid action: {action}")
        next_state = self.get_state(new_position)
        if self.grid[new_position] == StateKind.WALL.value:
            return self.state
        return next_state

    def to_str(self) -> str:
        symbols = np.vectorize(lambda x: StateKind(x).name[0])(self.grid)
        symbols = np.char.add(" ", np.char.add(symbols, " "))
        i, j = self.get_position(self.state)
        symbols[i, j] = f"[{StateKind(self.grid[i, j]).name[0]}]"
        return grid_str(symbols, self.width, self.height)


# Dummy example
if __name__ == "__main__":
    config = GridWorldConfig(
        width=5,
        height=5,
        start_states=[1],
        terminal_states=[24],
        cliff_states=[20, 21, 22, 23],
        wall_states=[7, 8, 9],
        random_seed=42,
    )
    grid_world = GridWorld(config)
    logger.debug(grid_world.to_str())

    for i in range(5):
        grid_world.step(Act.DOWN.value)
        logger.debug(grid_world.to_str())

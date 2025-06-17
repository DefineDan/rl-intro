import pytest
import numpy as np
from rl_intro.environment.gridworld import GridWorld, GridWorldConfig, Act, StateKind


@pytest.fixture
def grid_config() -> GridWorldConfig:
    return GridWorldConfig(
        width=4,
        height=4,
        start_states=[0],
        terminal_states=[15],
        cliff_states=[8, 9, 10],
        wall_states=[5, 6],
        random_seed=123,
    )


@pytest.fixture
def env(grid_config: GridWorldConfig) -> GridWorld:
    return GridWorld(grid_config)


def test_reset_returns_start_state(
    env: GridWorld, grid_config: GridWorldConfig
) -> None:
    state = env.reset()
    assert state in grid_config.start_states


def test_step_moves_agent(env: GridWorld) -> None:
    env.reset()
    s0 = env.state
    s1, reward, done = env.step(Act.RIGHT.value)
    assert s1 != s0
    assert isinstance(reward, float)
    assert isinstance(done, (bool, np.bool_))


def test_wall_blocks_movement(env: GridWorld) -> None:
    env.state = 4  # left of wall at 5
    s1, _, _ = env.step(Act.RIGHT.value)
    assert s1 == 4  # should not move into wall


def test_terminal_resets(env: GridWorld) -> None:
    env.state = 15  # terminal
    s1, _, _ = env.step(Act.UP.value)
    assert s1 in env.config.start_states


def test_cliff_resets(env: GridWorld) -> None:
    env.state = 10  # cliff
    s1, _, _ = env.step(Act.LEFT.value)
    assert s1 in env.config.start_states


def test_reward_function(env: GridWorld) -> None:
    env.state = 11
    _, reward, _ = env.step(Act.LEFT.value)
    assert reward == -100.0
    env.state = 11
    _, reward, _ = env.step(Act.DOWN.value)
    assert reward == 1.0
    env.state = 11  # empty
    _, reward, _ = env.step(Act.UP.value)
    assert reward == -1.0

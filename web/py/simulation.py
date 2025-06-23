from rl_intro.agent.core import AgentConfig
from rl_intro.agent.agent_expected_sarsa import AgentExpectedSarsa
from rl_intro.environment.gridworld import GridWorld, GridWorldConfig
from rl_intro.agent.policy import EpsilonGreedyPolicy, EpsilonGreedyConfig
from rl_intro.simulation.experiment import Experiment, ExperimentConfig
from rl_intro.utils.visualize import grid_str
from rl_intro.environment.gridworld import StateKind
from typing import List, Literal, Optional


def create_gridworld(grid: List[List], seed: Optional[int] = None) -> GridWorld:
    w = len(grid[0])
    h = len(grid)

    env_config = GridWorldConfig(
        width=w,
        height=h,
        start_states=[],
        terminal_states=[],
        cliff_states=[],
        wall_states=[],
        random_seed=seed,
    )
    for i in range(h):
        for j in range(w):
            state = i * w + j
            cell = grid[i][j]
            if cell == StateKind.START.value:
                env_config.start_states.append(state)
            elif cell == StateKind.TERMINAL.value:
                env_config.terminal_states.append(state)
            elif cell == StateKind.CLIFF.value:
                env_config.cliff_states.append(state)
            elif cell == StateKind.WALL.value:
                env_config.wall_states.append(state)
            elif cell == StateKind.EMPTY.value:
                continue
            else:
                raise ValueError(f"Invalid cell value {cell} at ({i}, {j})")

    return GridWorld(env_config)


def run_simulation(env: GridWorld):
    w, h = env.config.width, env.config.height

    agent_config = AgentConfig(
        n_states=w * h,
        n_actions=len(env.action_space),
        random_seed=42,
        learning_rate=0.3,
        discount=1.0,
    )
    agent = AgentExpectedSarsa(
        agent_config, EpsilonGreedyPolicy(EpsilonGreedyConfig(epsilon=0.1))
    )

    experiment_config = ExperimentConfig(n_episodes=1000, max_steps=200)
    experiment = Experiment(agent, env, experiment_config)

    log = []

    log.append("Before training:")
    log.append(env.to_str())
    log.append(grid_str(agent.get_greedy_actions(), w, h))
    log.append(grid_str(agent.get_greedy_values(), w, h))

    experiment.run()

    log.append("After training:")
    log.append(env.to_str())
    log.append(grid_str(agent.get_greedy_actions(), w, h))
    log.append(grid_str(agent.get_greedy_values(), w, h))

    global output, agent_pos
    output = "\n\n".join(log)
    position = env.get_position(env.state)
    agent_pos = {"row": int(position[0]), "col": int(position[1])}

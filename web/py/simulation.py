from rl_intro.agent.core import AgentConfig, Agent
from rl_intro.agent.agent_expected_sarsa import AgentExpectedSarsa
from rl_intro.agent.agent_q_learning import AgentQLearning
from rl_intro.agent.agent_sarsa import AgentSarsa
from rl_intro.environment.gridworld import GridWorld, GridWorldConfig
from rl_intro.agent.policy import EpsilonGreedyPolicy, EpsilonGreedyConfig
from rl_intro.simulation.experiment import Experiment, ExperimentConfig
from rl_intro.utils.visualize import grid_str
from rl_intro.environment.gridworld import StateKind
from typing import List, Literal, Optional
from enum import StrEnum


class AgentType(StrEnum):
    EXPECTED_SARSA = "expected_sarsa"
    Q_LEARNING = "q_learning"
    SARSA = "sarsa"


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


def create_agent(config: dict, n_states: int, n_actions: int) -> Agent:
    policy = EpsilonGreedyPolicy(
        EpsilonGreedyConfig(epsilon=config.get("epsilon", 0.1))
    )
    agent_config = AgentConfig(
        n_states=n_states,
        n_actions=n_actions,
        learning_rate=config.get("learning_rate", 0.1),
        discount=config.get("discount", 1.0),
        random_seed=42,
    )
    agent_type = AgentType(config.get("agent_type", "expected_sarsa"))
    if agent_type == AgentType.EXPECTED_SARSA:
        return AgentExpectedSarsa(agent_config, policy)
    elif agent_type == AgentType.Q_LEARNING:
        return AgentQLearning(agent_config, policy)
    elif agent_type == AgentType.SARSA:
        return AgentSarsa(agent_config, policy)
    else:
        raise ValueError(f"Invalid agent type: {agent_type}")


def run_simulation(env: GridWorld, agent: Agent):
    w, h = env.config.width, env.config.height

    experiment_config = ExperimentConfig(n_episodes=1000, max_steps=200)
    experiment = Experiment(agent, env, experiment_config)
    return experiment.run()


def get_current_position(env: GridWorld):
    position = env.get_position(env.state)
    return {"row": int(position[0]), "col": int(position[1])}
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
from rl_intro.evaluation.analyze import analyze_experiment
from dataclasses import asdict


########### ! GLOBAL VARIABLES FOR INTERFACING WITH PYODIDE
global_environment: Optional[GridWorld] = None
global_agent: Optional[Agent] = None
global_experiment: Optional[Experiment] = None
########### ! GLOBAL VARIABLES FOR INTERFACING WITH PYODIDE


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

    global global_environment
    global_environment = GridWorld(env_config)

    return global_environment


def create_agent(config: dict) -> Agent:
    if global_environment is None:
        raise ValueError("Environment not initialized. Cannot create agent")
    policy = EpsilonGreedyPolicy(
        EpsilonGreedyConfig(epsilon=config.get("epsilon", 0.1))
    )
    agent_config = AgentConfig(
        n_states=len(global_environment.state_space),
        n_actions=len(global_environment.action_space),
        learning_rate=config.get("learning_rate", 0.1),
        discount=config.get("discount", 1.0),
        random_seed=42,
    )
    agent_type = AgentType(config.get("agent_type", "expected_sarsa"))

    global global_agent
    if agent_type == AgentType.EXPECTED_SARSA:
        global_agent = AgentExpectedSarsa(agent_config, policy)
    elif agent_type == AgentType.Q_LEARNING:
        global_agent = AgentQLearning(agent_config, policy)
    elif agent_type == AgentType.SARSA:
        global_agent = AgentSarsa(agent_config, policy)
    else:
        raise ValueError(f"Invalid agent type: {agent_type}")
    return global_agent


def create_experiment(config: dict) -> Experiment:
    experiment_config = ExperimentConfig(
        n_episodes=config.get("n_episodes", 500),
        max_steps=config.get("max_steps", 200),
    )
    if global_agent is None or global_environment is None:
        raise ValueError("Agent or environment not initialized")
    global global_experiment
    global_experiment = Experiment(global_agent, global_environment, experiment_config)
    return global_experiment


def step_experiment():
    global global_experiment
    if global_experiment is None:
        raise ValueError("Experiment not initialized.")

    step_log = global_experiment.step()
    result = {
        "step_log": asdict(step_log),
        "position": get_current_position(),
        "values": get_current_values(),
    }
    return result


def run_full_experiment():
    if global_experiment is None:
        raise ValueError("Experiment not initialized")
    return global_experiment.run()


def analyze_experiment_logs():
    if global_experiment is None or global_environment is None:
        raise ValueError("Experiment not initialized")
    h, w = get_grid_shape()
    analysis = analyze_experiment(global_experiment.log, h, w)
    return {
        "cumulative_reward": analysis.cumulative_reward.to_json(orient="split"),
        "episodic_rewards": analysis.episodic_rewards.to_json(orient="split"),
        "values": analysis.final_values.flatten(),
        "visits": analysis.visit_matrix.flatten().astype(float),
    }


def get_current_values():
    if global_agent is None:
        raise ValueError("Cannot get values of None agent")
    return global_agent.get_greedy_values()


def get_grid_shape():
    if global_environment is None:
        raise ValueError("Cannot get shape of None env")
    return (global_environment.height, global_environment.width)


def get_current_position():
    if global_environment is None:
        raise ValueError("Cannot get position of None env")
    position = global_environment.get_position(global_environment.state)
    return {"row": int(position[0]), "col": int(position[1])}


def reset_globals():
    global global_environment
    global global_agent
    global global_experiment
    global_environment = None
    global_agent = None
    global_experiment = None

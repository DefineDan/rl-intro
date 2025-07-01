from rl_intro.agent.core import AgentConfig, Agent
from rl_intro.agent.agent_expected_sarsa import AgentExpectedSarsa
from rl_intro.agent.agent_q_learning import AgentQLearning
from rl_intro.agent.agent_sarsa import AgentSarsa
from rl_intro.environment.gridworld import GridWorld, GridWorldConfig
from rl_intro.agent.policy import EpsilonGreedyPolicy, EpsilonGreedyConfig
from rl_intro.simulation.experiment import Experiment, ExperimentConfig
from rl_intro.environment.gridworld import StateKind
from rl_intro.evaluation.analyze import analyze_experiment
from typing import List, Optional
from enum import StrEnum
from dataclasses import asdict

# Global registry for active simulations
_simulation_registry: dict[str, "Simulation"] = {}

class AgentType(StrEnum):
    EXPECTED_SARSA = "expected_sarsa"
    Q_LEARNING = "q_learning"
    SARSA = "sarsa"

class Simulation:
    def __init__(self, grid, agent_config, experiment_config):
        self.env = create_gridworld(grid)
        self.agent = create_agent(agent_config, self.env)
        self.experiment = create_experiment(experiment_config, self.agent, self.env)

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


def create_agent(config: dict, env: GridWorld) -> Agent:
    policy = EpsilonGreedyPolicy(
        EpsilonGreedyConfig(epsilon=config.get("epsilon", 0.1))
    )
    agent_config = AgentConfig(
        n_states=len(env.state_space),
        n_actions=len(env.action_space),
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


def create_experiment(config: dict, agent: Agent, env: GridWorld) -> Experiment:
    experiment_config = ExperimentConfig(
        n_episodes=config.get("n_episodes", 500),
        max_steps=config.get("max_steps", 200),
    )
    return Experiment(agent, env, experiment_config)


def create_simulation(sim_id, grid, agent_config, experiment_config):
    sim = Simulation(grid, agent_config, experiment_config)
    _simulation_registry[sim_id] = sim
    return sim_id

def get_simulation(sim_id) -> Simulation:
    if sim_id not in _simulation_registry:
        raise ValueError(f"Simulation with id {sim_id} not found.")
    return _simulation_registry[sim_id]

def step_experiment(sim_id):
    sim = get_simulation(sim_id)
    step_log = sim.experiment.step()
    result = {
        "step_log": asdict(step_log),
        "position": get_current_position(sim_id),
        "values": get_current_values(sim_id),
    }
    return result

def run_full_experiment(sim_id):
    sim = get_simulation(sim_id)
    return sim.experiment.run()

def get_current_values(sim_id):
    sim = get_simulation(sim_id)
    return sim.agent.get_greedy_values()

def get_grid_shape(sim_id):
    sim = get_simulation(sim_id)
    return (sim.env.height, sim.env.width)

def get_current_position(sim_id):
    sim = get_simulation(sim_id)
    position = sim.env.get_position(sim.env.state)
    return {"row": int(position[0]), "col": int(position[1])}

def analyze_experiment_logs(sim_id):
    sim = get_simulation(sim_id)
    h, w = get_grid_shape(sim_id)
    analysis = analyze_experiment(sim.experiment.log, h, w)
    return {
        "cumulative_reward": analysis.cumulative_reward.to_json(orient="split"),
        "episodic_rewards": analysis.episodic_rewards.to_json(orient="split"),
        "values": analysis.final_values.flatten(),
        "visits": analysis.visit_matrix.flatten().astype(float),
    }

def reset_simulation(sim_id):
    if sim_id in _simulation_registry:
        del _simulation_registry[sim_id]
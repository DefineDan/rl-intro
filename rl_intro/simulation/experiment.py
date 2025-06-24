from rl_intro.agent.core import Agent
from rl_intro.environment.core import Environment
from rl_intro.environment.core import State, Action, Reward, Terminal
from dataclasses import dataclass, asdict
from typing import Optional
from tqdm import trange
import json
from rl_intro.utils.logger import logger
from rl_intro.utils.visualize import grid_str

from rl_intro.agent.factory import AgentFactory, AgentRecipe
from rl_intro.environment.factory import EnvironmentFactory, EnvironmentRecipe


@dataclass
class ExperimentConfig:
    n_episodes: int = 1000
    max_steps: int = 100


@dataclass
class StepLog:
    episode: int
    step: int
    action: Action
    state: State
    reward: Reward
    terminal: Terminal


@dataclass
class ExperimentLog:
    id: int
    agent: str
    env: str
    experiment_config: ExperimentConfig
    steps: list[StepLog]
    final_values: Optional[list[float]] = None
    seed: Optional[int] = None


class Experiment:
    def __init__(
        self,
        agent: Agent,
        env: Environment,
        config: ExperimentConfig,
        id: int = 0,
    ):
        self.agent = agent
        self.env = env
        self.config = config
        self.log = ExperimentLog(
            id=id,
            agent=str(agent),
            env=str(env),
            experiment_config=self.config,
            steps=[],
            seed=agent.config.random_seed,
        )
        self.last_action: Optional[Action] = None
        self.episode_start: Terminal = True
        self.step_count: int = 0
        self.episode_count: int = 0

    def start_step(self) -> tuple[State, Reward, Terminal]:
        self.step_count = 0
        self.episode_count += 1
        state = self.env.reset()
        self.last_action = self.agent.step(state, None, False)
        self.episode_start = False
        return state, Reward(0.0), Terminal(False)  # track start step reward as 0.0

    def step(self) -> StepLog:
        if self.episode_start or self.last_action is None:
            state, reward, terminal = self.start_step()
        else:
            state, reward, terminal = self.env.step(self.last_action)
            self.last_action = self.agent.step(state, reward, terminal)
            self.step_count += 1
            self.episode_start = terminal or self.step_count >= self.config.max_steps
        assert self.last_action is not None, "Agent did not return an action."
        step_log = StepLog(
            episode=self.episode_count,
            step=self.step_count,
            action=self.last_action,
            state=state,
            reward=reward,
            terminal=terminal,
        )
        self.log.steps.append(step_log)
        return step_log

    def run_episode(self) -> None:
        while True:
            self.step()
            if self.episode_start:
                break

    def run_episodes(self, n_episodes: int) -> ExperimentLog:
        for _ in trange(n_episodes, desc="Episodes"):
            self.run_episode()
        self.log.final_values = self.agent.get_greedy_values().tolist()
        return self.log

    def run(self) -> ExperimentLog:
        assert len(self.log.steps) == 0, "Experiment log is not empty."
        return self.run_episodes(self.config.n_episodes)


class ExperimentBatch:
    def __init__(
        self,
        agent_recipes: list[AgentRecipe],
        env_recipes: list[EnvironmentRecipe],
        experiment_config: ExperimentConfig,
        n_runs: int,
    ):
        self.agent_recipes = agent_recipes
        self.env_recipes = env_recipes
        self.experiment_config = experiment_config
        self.n_runs = n_runs
        self.experiment_logs: list[ExperimentLog] = []

    def run(self) -> list[ExperimentLog]:
        # TODO: multithreading support
        for i_run in trange(self.n_runs, desc="Runs"):
            random_seed = i_run
            for env_recipe in self.env_recipes:
                env = EnvironmentFactory.create_environment(
                    env_recipe, seed_override=random_seed
                )
                for agent_recipe in self.agent_recipes:
                    agent = AgentFactory.create_agent(
                        agent_recipe, seed_override=random_seed
                    )
                    experiment = Experiment(
                        agent, env, self.experiment_config, id=i_run
                    )
                    logger.info(
                        f"Running experiment {i_run + 1}/{self.n_runs} with agent {agent} and environment {env}."
                    )
                    experiment_log = experiment.run()
                    self.experiment_logs.append(experiment_log)
        return self.experiment_logs


if __name__ == "__main__":
    # Example usage
    from rl_intro.agent.core import AgentConfig
    from rl_intro.agent.agent_sarsa import AgentSarsa
    from rl_intro.agent.agent_q_learning import AgentQLearning
    from rl_intro.agent.agent_expected_sarsa import AgentExpectedSarsa

    from rl_intro.environment.gridworld import GridWorld, GridWorldConfig
    from rl_intro.agent.policy import EpsilonGreedyPolicy, EpsilonGreedyConfig
    from pathlib import Path

    w, h = 10, 4
    out_dir = Path(__file__).parent.parent.parent / "data"

    env_config = GridWorldConfig(
        width=w,
        height=h,
        start_states=[0],
        terminal_states=[39],
        cliff_states=[4, 24, 5, 25],
        wall_states=[2, 12, 22, 17, 27, 37],
        random_seed=42,
    )
    env = GridWorld(env_config)

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

    logger.info(f"Agent: {agent}")
    logger.debug(env.to_str())
    logger.debug(agent.policy.get_distribution(agent))
    logger.debug(grid_str(agent.get_greedy_actions(), w, h))
    logger.debug(grid_str(agent.get_greedy_values(), w, h))

    # ! running the experiment
    experiment_log = experiment.run()

    logger.debug(env.to_str())
    logger.debug(agent.policy.get_distribution(agent))
    logger.debug(grid_str(agent.get_greedy_actions(), w, h))
    logger.debug(grid_str(agent.get_greedy_values(), w, h))

    # save the logs as a json file
    with open(out_dir / "experiment_logs.json", "w") as f:
        json.dump(asdict(experiment_log), f, indent=4)
    logger.info("Experiment completed and logs saved to 'experiment_logs.json'.")

    agent_recipe = AgentRecipe(
        agent_class=AgentExpectedSarsa,
        agent_config=agent_config,
        policy_class=EpsilonGreedyPolicy,
        policy_config=EpsilonGreedyConfig(epsilon=0.1),
    )
    env_recipe = EnvironmentRecipe(
        environment_class=GridWorld,
        environment_config=env_config,
    )
    experiment_batch = ExperimentBatch(
        agent_recipes=[agent_recipe],
        env_recipes=[env_recipe],
        experiment_config=experiment_config,
        n_runs=5,
    )
    logs = experiment_batch.run()
    # Save all logs to a JSON file

    with open(out_dir / "experiment_batch_logs.json", "w") as f:
        json.dump(
            [asdict(log) for log in logs], f, indent=4, default=lambda o: o.__dict__
        )

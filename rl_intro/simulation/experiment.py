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
    agent: str
    env: str
    experiment_config: ExperimentConfig
    steps: list[StepLog]
    final_values: Optional[list[float]] = None


class Experiment:
    def __init__(self, agent: Agent, env: Environment, config: ExperimentConfig):
        self.agent = agent
        self.env = env
        self.config = config
        self.log = ExperimentLog(
            agent=str(agent),
            env=str(env),
            experiment_config=self.config,
            steps=[],
        )

    def run_episodes(self, n_episodes: int, max_steps: int) -> ExperimentLog:
        for episode in trange(n_episodes, desc="Episodes"):
            self.env.reset()
            action = self.agent.start(self.env.state)
            for step in range(1, max_steps + 1):
                state, reward, terminal = self.env.step(action)
                self.log.steps.append(
                    StepLog(
                        episode=episode,
                        step=step,
                        action=Action(action),
                        state=State(state),
                        reward=Reward(reward),
                        terminal=Terminal(terminal),
                    )
                )
                action = self.agent.step(state, reward, terminal)
                if terminal:
                    break
            else:
                logger.warning(
                    f"Agent took too many steps ({self.config.max_steps}) in episode {episode}, resetting."
                )
        self.log.final_values = self.agent.get_greedy_values().tolist()
        return self.log

    def run(self) -> ExperimentLog:
        assert len(self.log.steps) == 0, "Experiment log is not empty."
        return self.run_episodes(self.config.n_episodes, self.config.max_steps)


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
                    experiment = Experiment(agent, env, experiment_config)
                    logger.info(
                        f"Running experiment {i_run + 1}/{self.n_runs} with agent {agent} and environment {env}."
                    )
                    experiment_log = experiment.run()
                    self.experiment_logs.append(experiment_log)
        return self.experiment_logs


if __name__ == "__main__":
    # Example usage
    from rl_intro.agent.agent_sarsa import AgentSarsa, AgentSarsaConfig
    from rl_intro.environment.gridworld import GridWorld, GridWorldConfig
    from rl_intro.agent.policy import EpsilonGreedyPolicy, EpsilonGreedyConfig

    w, h = 10, 4

    env_config = GridWorldConfig(
        width=w,
        height=h,
        start_states=[0],
        terminal_states=[9],
        cliff_states=[1, 2, 3, 4, 5, 6, 7, 8],
        wall_states=[],
        random_seed=42,
    )
    env = GridWorld(env_config)

    agent_config = AgentSarsaConfig(
        n_states=w * h,
        n_actions=len(env.action_space),
        random_seed=42,
        learning_rate=0.3,
        discount=1.0,
    )
    agent = AgentSarsa(
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
    with open("experiment_logs.json", "w") as f:
        json.dump(asdict(experiment_log), f, indent=4)
    logger.info("Experiment completed and logs saved to 'experiment_logs.json'.")

    agent_recipe = AgentRecipe(
        agent_class=AgentSarsa,
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

    with open("experiment_batch_logs.json", "w") as f:
        json.dump(
            [asdict(log) for log in logs], f, indent=4, default=lambda o: o.__dict__
        )

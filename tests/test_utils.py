import numpy as np
from rl_intro.agent.core import Policy, PolicyConfig
from rl_intro.agent.core import Agent, AgentConfig


class DummyPolicy(Policy):
    def __init__(self, config=None):
        if config is None:
            config = PolicyConfig()
        self.config = config

    def select_action(self, agent, state, reward):
        return 0  # Always return action 0

    def get_distribution(self, agent):
        return (
            np.ones((agent.config.n_states, agent.config.n_actions))
            / agent.config.n_actions
        )

    def get_state_distribution(self, agent, state):
        return np.ones(agent.config.n_actions) / agent.config.n_actions


class DummyAgent(Agent):
    def __init__(self, n_states=10, n_actions=5, q=None, random_generator=None):
        self.config = AgentConfig(
            n_states=n_states, n_actions=n_actions, random_seed=41
        )
        self.policy = DummyPolicy(PolicyConfig())
        self.q = np.zeros((n_states, n_actions)) if q is None else q
        self.random_generator = random_generator or np.random.default_rng(
            self.config.random_seed
        )

    def start(self, state, *a, **kw):
        return 0

    def step(self, state, reward, terminal):
        return 0

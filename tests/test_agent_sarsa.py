import pytest
import numpy as np
from rl_intro.agent.agent_sarsa import AgentSarsa, AgentSarsaConfig
from rl_intro.agent.core import Policy, PolicyConfig
from rl_intro.environment.core import State, Action, Reward, Terminal


class DummyPolicy(Policy):
    def select_action(self, agent, state, reward):
        return 0  # Always return action 0

    def get_distribution(self, agent):
        # Return uniform distribution as a stub
        return (
            np.ones((agent.config.n_states, agent.config.n_actions))
            / agent.config.n_actions
        )


def make_agent(n_states=3, n_actions=2, seed=42):
    config = AgentSarsaConfig(n_states=n_states, n_actions=n_actions, random_seed=seed)
    return AgentSarsa(config, DummyPolicy(PolicyConfig()))


def test_learn_non_terminal():
    agent = make_agent()
    agent.last_state = 0
    agent.last_action = 0
    agent.q[0, 0] = 1.0
    agent.q[1, 0] = 2.0
    reward = 0.5
    terminal = False
    next_state = 1
    next_action = 0
    agent.learn(next_state, reward, terminal, next_action)
    expected = 1.0 + agent.config.learning_rate * (
        reward + agent.config.discount * 2.0 - 1.0
    )
    assert np.isclose(agent.q[0, 0], expected)


def test_learn_terminal():
    agent = make_agent()
    agent.last_state = 0
    agent.last_action = 0
    agent.q[0, 0] = 1.0
    reward = 0.5
    terminal = True
    next_state = 1
    next_action = 0
    agent.learn(next_state, reward, terminal, next_action)
    expected = 1.0 + agent.config.learning_rate * (reward - 1.0)
    assert np.isclose(agent.q[0, 0], expected)


def test_step_updates_q():
    agent = make_agent()
    state0 = 0
    state1 = 1
    reward = 1.0
    terminal = False
    agent.start(state0)
    agent.q[state0, 0] = 0.0
    agent.q[state1, 0] = 2.0
    action = agent.step(state1, reward, terminal)
    expected = 0.0 + agent.config.learning_rate * (
        reward + agent.config.discount * 2.0 - 0.0
    )
    assert np.isclose(agent.q[state0, 0], expected)
    assert action == 0

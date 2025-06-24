import pytest
import numpy as np
from rl_intro.agent.agent_expected_sarsa import AgentExpectedSarsa, AgentConfig
from rl_intro.agent.core import PolicyConfig
from rl_intro.environment.core import State, Action, Reward, Terminal
from tests.test_utils import DummyPolicy


def make_agent(n_states=3, n_actions=2, seed=42):
    config = AgentConfig(n_states=n_states, n_actions=n_actions, random_seed=seed)
    return AgentExpectedSarsa(config, DummyPolicy(PolicyConfig()))


def test_learn_non_terminal():
    agent = make_agent()
    agent.last_state = 0
    agent.last_action = 0
    agent.q[0, 0] = 1.0
    agent.q[1, 0] = 2.0
    agent.q[1, 1] = 4.0
    reward = 0.5
    terminal = False
    next_state = 1
    next_action = 0  # Not used in Expected SARSA
    # Expected value: mean of q[1, :] = (2.0 + 4.0) / 2 = 3.0
    agent.learn(next_state, reward, terminal, next_action)
    expected = 1.0 + agent.config.learning_rate * (
        reward + agent.config.discount * 3.0 - 1.0
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
    agent.step(state0, 0, False)
    agent.q[state0, 0] = 0.0
    agent.q[state1, 0] = 2.0
    agent.q[state1, 1] = 4.0
    # Expected value: mean of q[state1, :] = (2.0 + 4.0) / 2 = 3.0
    action = agent.step(state1, reward, terminal)
    expected = 0.0 + agent.config.learning_rate * (
        reward + agent.config.discount * 3.0 - 0.0
    )
    assert np.isclose(agent.q[state0, 0], expected)
    assert action == 0

import numpy as np
import pytest
from unittest.mock import MagicMock
from rl_intro.agent.policy import (
    RandomPolicy,
    EpsilonGreedyPolicy,
    EpsilonGreedyConfig,
    PolicyConfig,
)
from tests.test_utils import DummyAgent


def test_random_policy_select_action():
    # Mock random choice to always return 2
    expected_action = 2
    state = 2  # Dummy state

    mock_rng = MagicMock()
    mock_rng.choice.return_value = expected_action
    agent = DummyAgent(random_generator=mock_rng)
    agent.q[state, 1] = 10
    policy = RandomPolicy(config=PolicyConfig())
    action = policy.select_action(agent, state, None)
    assert action == expected_action
    mock_rng.choice.assert_called_with(agent.config.n_actions)


def test_random_policy_distribution():
    agent = DummyAgent()
    policy = RandomPolicy(config=PolicyConfig())
    dist = policy.get_distribution(agent)
    assert np.allclose(dist, 1.0 / agent.config.n_actions)


def test_epsilon_greedy_policy_explore():
    # Force random() < epsilon, so always explore
    expected_action = 1
    state = 2  # Dummy state

    mock_rng = MagicMock()
    mock_rng.random.return_value = 0.05
    mock_rng.choice.return_value = expected_action
    agent = DummyAgent(random_generator=mock_rng)
    agent.q[state, 2] = 10  # should not be chosen
    policy = EpsilonGreedyPolicy(EpsilonGreedyConfig(epsilon=0.1))
    action = policy.select_action(agent, state, None)
    mock_rng.random.assert_called()
    mock_rng.choice.assert_called_with(agent.config.n_actions)
    assert action == expected_action


def test_epsilon_greedy_policy_exploit():
    # Force random() >= epsilon, so always exploit
    expected_action = 1
    state = 2  # Dummy state

    mock_rng = MagicMock()
    mock_rng.random.return_value = 0.11
    mock_rng.choice.return_value = expected_action  # fair_argmax will call this
    agent = DummyAgent(random_generator=mock_rng)
    agent.q[state, expected_action] = 10  # should be chosen
    policy = EpsilonGreedyPolicy(EpsilonGreedyConfig(epsilon=0.1))
    action = policy.select_action(agent, state, None)
    mock_rng.random.assert_called()
    mock_rng.choice.assert_called_with([expected_action])
    assert action == expected_action


def test_epsilon_greedy_policy_exploit_ties():
    expected_action = 1
    other_max_action = 2
    state = 2  # Dummy state

    mock_rng = MagicMock()
    mock_rng.random.return_value = 0.11
    mock_rng.choice.return_value = expected_action  # fair_argmax will call this
    agent = DummyAgent(random_generator=mock_rng)
    agent.q[state, expected_action] = 10  # should be chosen
    agent.q[state, other_max_action] = 10  # tie with another action
    policy = EpsilonGreedyPolicy(EpsilonGreedyConfig(epsilon=0.1))
    action = policy.select_action(agent, state, None)
    mock_rng.random.assert_called()
    called_args, _ = mock_rng.choice.call_args
    np.testing.assert_array_equal(
        np.sort(called_args[0]), np.array([expected_action, other_max_action])
    )
    assert action == expected_action


def test_epsilon_greedy_policy_distribution_ties():
    q = np.array([[1, 2, 2, 0]])
    agent = DummyAgent(q=q, n_states=1, n_actions=4)
    config = EpsilonGreedyConfig(epsilon=0.2)
    policy = EpsilonGreedyPolicy(config)
    dist = policy.get_distribution(agent)
    expected = np.array([[0.05, 0.45, 0.45, 0.05]])
    assert np.allclose(dist, expected)

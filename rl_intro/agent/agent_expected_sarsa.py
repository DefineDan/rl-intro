from rl_intro.agent.core import Agent, AgentConfig, Policy
from rl_intro.environment.core import Reward, Action, Terminal, State
from typing import Optional
import numpy as np
from rl_intro.utils.logger import logger

# TODO: use as base for sarsa and q-learning as its a generalization of both
# TODO: fix action space indexing (assuming 0-indexed actions here)


class AgentExpectedSarsa(Agent):
    def __init__(self, config: AgentConfig, policy: Policy):
        self.config = config
        self.policy = policy

        self.last_state: Optional[State] = None
        self.last_action: Optional[Action] = None

        self.q = np.zeros((self.config.n_states, self.config.n_actions))
        self.random_generator = np.random.default_rng(config.random_seed)

        logger.debug(self.__str__() + " initialized.")

    def __str__(self):
        return f"AgentExpectedSarsa(learning_rate={self.config.learning_rate},discount={self.config.discount},policy={self.policy})"

    def step(
        self, state: State, reward: Optional[Reward], terminal: Terminal
    ) -> Action:
        action = self.policy.select_action(self, state, reward)
        if reward is not None:
            self.learn(state, reward, terminal, action)
        self.last_state = state if not terminal else None
        self.last_action = action if not terminal else None
        return action

    def learn(
        self, state: State, reward: Reward, terminal: Terminal, action: Action
    ) -> None:
        if terminal:
            td_error = reward - self.q[self.last_state, self.last_action]
        else:
            expected_value = np.dot(
                self.policy.get_state_distribution(self, state), self.q[state, :]
            )
            td_error = (
                reward
                + self.config.discount * expected_value
                - self.q[self.last_state, self.last_action]
            )
        self.q[self.last_state, self.last_action] += (
            self.config.learning_rate * td_error
        )

from rl_intro.agent.core import Agent
from rl_intro.agent.core import AgentConfig, Policy
from rl_intro.agent.policy import EpsilonGreedyPolicy, EpsilonGreedyConfig
from rl_intro.agent.agent_q import QLearningAgent, QAgentConfig


def create(
    agent_class: type[Agent], policy_class: type[Policy], agent_config: AgentConfig
) -> Agent:
    """
    Factory function to create an agent with a specific policy.
    """
    policy = policy_class(agent_config.policy_config)
    return agent_class(agent_config, policy)


if __name__ == "__main__":
    # Example usage
    policy_config = EpsilonGreedyConfig(epsilon=0.1)
    agent_config = QAgentConfig(
        state_space=list(range(16)),
        action_space=list(
            range(4)
        ),  # Example action space (0-3 for UP, DOWN, LEFT, RIGHT)
        policy_config=policy_config,
        random_seed=42,
    )
    agent = create(QLearningAgent, EpsilonGreedyPolicy, agent_config)
    print(agent.q)  # Should print the initialized Q-table

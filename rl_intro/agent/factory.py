from rl_intro.agent.core import AgentConfig, Policy, PolicyConfig, Agent
from rl_intro.agent.policy import EpsilonGreedyPolicy, EpsilonGreedyConfig
from rl_intro.agent.agent_q import QLearningAgent, QAgentConfig
from dataclasses import dataclass


@dataclass
class AgentRecipe:
    agent_class: type[Agent]
    policy_class: type[Policy]
    agent_config: AgentConfig
    policy_config: PolicyConfig


class AgentFactory:
    @staticmethod
    def create_agent(recipe: AgentRecipe) -> Agent:
        policy = recipe.policy_class(recipe.policy_config)
        return recipe.agent_class(recipe.agent_config, policy)

    @staticmethod
    def create_agents(recipes: list[AgentRecipe]) -> list[Agent]:
        return [AgentFactory.create_agent(r) for r in recipes]


if __name__ == "__main__":
    # Example usage
    policy_config = EpsilonGreedyConfig(epsilon=0.1)
    agent_config = QAgentConfig(
        state_space=list(range(16)),
        action_space=list(range(4)),
        random_seed=42,
    )
    recipe = AgentRecipe(
        agent_class=QLearningAgent,
        agent_config=QAgentConfig(
            state_space=list(range(16)),
            action_space=list(range(4)),
            random_seed=42,
        ),
        policy_class=EpsilonGreedyPolicy,
        policy_config=EpsilonGreedyConfig(epsilon=0.1),
    )
    agent = AgentFactory.create_agent(recipe)
    print(agent.q)  # Should print the initialized Q-table

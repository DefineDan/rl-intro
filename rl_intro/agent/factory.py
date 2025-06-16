from rl_intro.agent.core import AgentConfig, Policy, PolicyConfig, Agent
from rl_intro.agent.policy import EpsilonGreedyPolicy, EpsilonGreedyConfig
from rl_intro.agent.agent_q import QLearningAgent, QAgentConfig
from rl_intro.agent.agent_sarsa import AgentSarsa, AgentSarsaConfig
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
    recipe = AgentRecipe(
        agent_class=AgentSarsa,
        agent_config=AgentSarsaConfig(
            n_states=10,
            n_actions=4,
            random_seed=42,
            learning_rate=0.1,
            discount=0.9,
        ),
        policy_class=EpsilonGreedyPolicy,
        policy_config=EpsilonGreedyConfig(epsilon=0.1),
    )
    agent = AgentFactory.create_agent(recipe)
    print(agent.q)  # Should print the initialized Q-table
    a = agent.start(0)  # Start with an initial state
    print(f"Initial action: {a}")  # Should print the initial action chosen by the agent

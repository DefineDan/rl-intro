from rl_intro.agent.core import AgentConfig, Policy, PolicyConfig, Agent
from rl_intro.agent.policy import EpsilonGreedyPolicy, EpsilonGreedyConfig
from dataclasses import dataclass
from typing import Optional
from rl_intro.utils.logger import logger


@dataclass
class AgentRecipe:
    agent_class: type[Agent]
    policy_class: type[Policy]
    agent_config: AgentConfig
    policy_config: PolicyConfig


class AgentFactory:
    @staticmethod
    def create_agent(recipe: AgentRecipe, seed_override: Optional[int] = None) -> Agent:
        if seed_override is not None:
            recipe.agent_config.random_seed = seed_override
        return recipe.agent_class(
            recipe.agent_config, recipe.policy_class(recipe.policy_config)
        )

    @staticmethod
    def create_agents(recipes: list[AgentRecipe]) -> list[Agent]:
        return [AgentFactory.create_agent(r) for r in recipes]


# * Example usage
if __name__ == "__main__":
    from rl_intro.agent.agent_sarsa import AgentSarsa

    recipe = AgentRecipe(
        agent_class=AgentSarsa,
        agent_config=AgentConfig(
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
    logger.debug(agent)
    logger.debug(f"Initial action: {agent.step(0, None, False)}")

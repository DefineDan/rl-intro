from rl_intro.environment.core import Environment, EnvironmentConfig
from dataclasses import dataclass, asdict
from typing import Type, List
from rl_intro.utils.logger import logger
from typing import Optional


@dataclass
class EnvironmentRecipe:
    environment_class: Type[Environment]
    environment_config: EnvironmentConfig


class EnvironmentFactory:
    @staticmethod
    def create_environment(
        recipe: EnvironmentRecipe, seed_override: Optional[int] = None
    ) -> Environment:
        if seed_override is not None:
            recipe.environment_config.random_seed = seed_override
        return recipe.environment_class(recipe.environment_config)

    @staticmethod
    def create_environments(recipes: List[EnvironmentRecipe]) -> List[Environment]:
        return [EnvironmentFactory.create_environment(r) for r in recipes]


# * Example usage
if __name__ == "__main__":
    from rl_intro.environment.gridworld import GridWorld, GridWorldConfig

    recipe = EnvironmentRecipe(
        environment_class=GridWorld,
        environment_config=GridWorldConfig(
            width=5,
            height=5,
            random_seed=42,
            start_states=[0],
            terminal_states=[24],
            cliff_states=[],
            wall_states=[],
        ),
    )
    env = EnvironmentFactory.create_environment(recipe)
    logger.debug(env.to_str())

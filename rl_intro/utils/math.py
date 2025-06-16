import numpy as np
from numpy.typing import NDArray, ArrayLike
from typing import Any

# import arraylike


def fair_argmax(x: ArrayLike, random_generator: np.random.Generator) -> tuple[int, Any]:
    """
    Returns a random index of the maximum value in the array.
    If there are multiple maximum values, it randomly selects one of them.
    """
    max_value = np.max(x)
    max_indices = np.where(x == max_value)[0]
    return random_generator.choice(max_indices), max_value

import numpy as np


def grid_str(arr: np.ndarray, width: int, height: int) -> str:
    """Returns a string representation of a 2D grid represented by a 1D array or 2D array."""
    if isinstance(arr, np.ndarray) and arr.ndim == 2:
        arr = arr.flatten()
    assert len(arr) == width * height, "Array length does not match grid dimensions."

    def format_elem(x):
        if isinstance(x, float):
            return f"{x:5.1f}"
        elif isinstance(x, int):
            return f"{x:5d}"
        return str(x)

    lines = []
    for i in range(height):
        row = arr[i * width : (i + 1) * width]
        lines.append(" ".join(format_elem(x) for x in row))
    return "\n" + "\n".join(lines) + "\n"

import pandas as pd
import numpy as np


def cumulative_reward(df: pd.DataFrame) -> None:
    df["cumulative_reward"] = df["reward"].cumsum()


def episodic_rewards(df: pd.DataFrame) -> pd.DataFrame:
    episodic_rewards = df.groupby("episode")["reward"].sum().reset_index()
    return episodic_rewards


def state_visit_frequency(df: pd.DataFrame, n_states: int) -> pd.DataFrame:
    state_visits = df.groupby("state").size().reset_index(name="num_visits")
    state_visits = state_visits.set_index("state").reindex(
        range(n_states), fill_value=0
    )
    return state_visits


def state_visit_frequency_matrix(
    df: pd.DataFrame, n_rows: int, n_cols: int
) -> np.ndarray:
    state_visits = state_visit_frequency(df, n_rows * n_cols)
    visit_matrix = state_visits["num_visits"].to_numpy().reshape((n_rows, n_cols))
    return visit_matrix


def final_values_matrix(
    final_values: list[float], n_rows: int, n_cols: int
) -> np.ndarray:
    values = np.array(final_values).reshape((n_rows, n_cols))
    return values


def average_experiments_time_series(
    dfs: list[pd.DataFrame], column: str, index_column: str
) -> pd.DataFrame:
    """Compute the mean of a time series column across multiple DataFrames, ensuring alignment by index_column."""

    # Check alignment by index_column
    reference_steps = dfs[0][index_column]
    for i, df in enumerate(dfs[1:], start=1):
        if not reference_steps.equals(df[index_column]):
            raise ValueError(
                f"DataFrame at index {i} has mismatched '{index_column}' values."
            )

    # Set index to 'global_step' for alignment
    series_list = [df.set_index(index_column)[column] for df in dfs]
    combined = pd.concat(series_list, axis=1)
    averaged = combined.mean(axis=1)
    return averaged.reset_index(name=column)


def average_experiments_matrix(matrices: list[np.ndarray]) -> np.ndarray:
    """Compute the mean of a matrix across multiple matrices."""
    shapes = [m.shape for m in matrices]
    if not all(shape == shapes[0] for shape in shapes):
        raise ValueError("All matrices must have the same shape for averaging.")
    return np.mean(np.array(matrices), axis=0)

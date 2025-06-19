import pandas as pd
import numpy as np
from rl_intro.simulation.experiment import ExperimentLog
from rl_intro.evaluation.parse import to_dataframe
from dataclasses import dataclass


@dataclass
class AnalysisResult:
    agent: str
    cumulative_reward: pd.DataFrame
    episodic_rewards: pd.DataFrame
    visit_matrix: np.ndarray
    final_values: np.ndarray


def calc_cumulative_reward(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        {"global_step": df["global_step"], "cumulative_reward": df["reward"].cumsum()}
    )


def calc_episodic_rewards(df: pd.DataFrame) -> pd.DataFrame:
    episodic_rewards = df.groupby("episode")["reward"].sum().reset_index()
    return episodic_rewards


def calc_state_visit_frequency(df: pd.DataFrame, n_states: int) -> pd.DataFrame:
    state_visits = df.groupby("state").size().reset_index(name="num_visits")
    state_visits = state_visits.set_index("state").reindex(
        range(n_states), fill_value=0
    )
    return state_visits


def gen_state_visit_frequency_matrix(
    df: pd.DataFrame, n_rows: int, n_cols: int
) -> np.ndarray:
    state_visits = calc_state_visit_frequency(df, n_rows * n_cols)
    visit_matrix = state_visits["num_visits"].to_numpy().reshape((n_rows, n_cols))
    return visit_matrix


def gen_final_values_matrix(
    final_values: list[float], n_rows: int, n_cols: int
) -> np.ndarray:
    values = np.array(final_values).reshape((n_rows, n_cols))
    return values


def average_experiments_time_series(
    dfs: list[pd.DataFrame], column: str, index_column: str
) -> pd.DataFrame:
    """Compute the mean of a time series column across multiple DataFrames."""
    series_list = [df.set_index(index_column)[column] for df in dfs]
    combined = pd.concat(series_list, axis=1)
    averaged = combined.mean(axis=1, skipna=True)

    return averaged.reset_index(name=column)


def average_experiments_matrix(matrices: list[np.ndarray]) -> np.ndarray:
    """Compute the mean of a matrix across multiple matrices."""
    shapes = [m.shape for m in matrices]
    if not all(shape == shapes[0] for shape in shapes):
        raise ValueError("All matrices must have the same shape for averaging.")
    return np.mean(np.array(matrices), axis=0)


def group_by_agent(experiments: list[ExperimentLog]) -> dict[str, list[ExperimentLog]]:
    agents = set(e.agent for e in experiments)
    return {agent: [e for e in experiments if e.agent == agent] for agent in agents}


def analyze_experiment(
    experiment_log: ExperimentLog, n_rows: int, n_cols: int
) -> AnalysisResult:
    df = to_dataframe(experiment_log)
    return AnalysisResult(
        agent=experiment_log.agent,
        cumulative_reward=calc_cumulative_reward(df),
        episodic_rewards=calc_episodic_rewards(df),
        visit_matrix=gen_state_visit_frequency_matrix(df, n_rows, n_cols),
        final_values=(
            gen_final_values_matrix(experiment_log.final_values, n_rows, n_cols)
            if experiment_log.final_values
            else np.zeros((n_rows, n_cols))
        ),
    )


def analyze_experiment_group(
    experiments: list[ExperimentLog], n_rows: int, n_cols: int
) -> AnalysisResult:
    """Averages results from multiple experiments."""
    results = [analyze_experiment(exp, n_rows, n_cols) for exp in experiments]
    return AnalysisResult(
        agent=experiments[0].agent,
        cumulative_reward=average_experiments_time_series(
            [res.cumulative_reward for res in results],
            column="cumulative_reward",
            index_column="global_step",
        ),
        episodic_rewards=average_experiments_time_series(
            [res.episodic_rewards for res in results],
            column="reward",
            index_column="episode",
        ),
        visit_matrix=average_experiments_matrix([res.visit_matrix for res in results]),
        final_values=average_experiments_matrix([res.final_values for res in results]),
    )


def analyze_experiments(
    experiments: list[ExperimentLog], n_rows: int, n_cols: int
) -> dict[str, AnalysisResult]:
    """Analyze a list of ExperimentLog objects, grouping by agent and averaging results."""
    grouped_experiments = group_by_agent(experiments)
    return {
        agent: analyze_experiment_group(exp_group, n_rows, n_cols)
        for agent, exp_group in grouped_experiments.items()
    }


if __name__ == "__main__":
    from pathlib import Path
    from rl_intro.evaluation.parse import parse_experiment_batch_json

    file_path = Path("experiment_batch_logs.json")
    batch_experiment_logs = parse_experiment_batch_json(file_path)

    n_rows, n_cols = 4, 10
    analysis = analyze_experiments(batch_experiment_logs, n_rows=n_rows, n_cols=n_cols)

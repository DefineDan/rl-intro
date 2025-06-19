from typing import Optional, Dict, List
import matplotlib.pyplot as plt
import numpy as np
from rl_intro.evaluation.analyze import AnalysisResult

plt.style.use("dark_background")


def shorten_agent_name(agent: str) -> str:
    return agent.split("(")[0]


def _process_series(series, interval=None, running_mean=None):
    """Utility to slice and smooth a 1D numpy array or pandas Series."""
    if interval:
        start, end = interval
        series = series[start:end]
    if running_mean is not None and running_mean > 1:
        series = np.convolve(series, np.ones(running_mean) / running_mean, mode="valid")
    return series


def plot_cumulative_reward(
    results: Dict[str, AnalysisResult],
    ax,
    interval: Optional[tuple[int, int]] = None,
    running_mean: Optional[int] = None,
):
    """Plot cumulative reward time series for each agent/result, with optional running mean."""
    for agent, res in results.items():
        steps = _process_series(
            res.cumulative_reward["global_step"], interval, running_mean
        )
        rewards = _process_series(
            res.cumulative_reward["cumulative_reward"], interval, running_mean
        )
        # If running_mean is used, steps and rewards may be different lengths; align steps
        if running_mean is not None and running_mean > 1:
            steps = steps[: len(rewards)]
        ax.plot(steps, rewards, label=shorten_agent_name(agent), alpha=1.0)
    ax.set_title("Cumulative Reward Over Time")
    ax.set_xlabel("Steps")
    ax.set_ylabel("Cumulative Reward")
    ax.grid(True, alpha=0.2)
    ax.legend()
    return ax.get_figure(), ax


def plot_average_reward_per_episode(
    results: Dict[str, AnalysisResult],
    ax,
    interval: Optional[tuple[int, int]] = None,
    running_mean: Optional[int] = None,
):
    """Plot average reward per episode for each agent/result, with optional running mean."""
    for agent, res in results.items():
        episodes = _process_series(
            res.episodic_rewards["episode"], interval, running_mean
        )
        rewards = _process_series(
            res.episodic_rewards["reward"], interval, running_mean
        )
        if running_mean is not None and running_mean > 1:
            episodes = episodes[: len(rewards)]
        ax.plot(episodes, rewards, label=shorten_agent_name(agent), alpha=0.9)
    ax.set_title("Average Reward Per Episode")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Average Reward")
    ax.grid(True, alpha=0.2)
    ax.legend()
    return ax.get_figure(), ax


def plot_final_values(result: AnalysisResult, ax):
    """Display the final values matrix for a single result."""
    values = result.final_values
    cax = ax.imshow(values, cmap="viridis", interpolation="nearest")
    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            val = values[i, j]
            ax.text(
                j,
                i,
                f"{val:.1f}",
                ha="center",
                va="center",
                color="white" if val < 0.5 else "black",
            )
    ax.set_title(f"Final Values: {shorten_agent_name(result.agent)}")
    ax.figure.colorbar(cax, ax=ax, orientation="horizontal")
    return ax.get_figure(), ax


def plot_state_visit_frequency(result: AnalysisResult, ax):
    """Display the state visit frequency matrix for a single result."""
    visit_array = result.visit_matrix
    cax = ax.imshow(visit_array, cmap="viridis", interpolation="nearest")
    ax.figure.colorbar(cax, ax=ax, orientation="horizontal")
    ax.set_title(f"State Visit Frequency: {shorten_agent_name(result.agent)}")
    return ax.get_figure(), ax


if __name__ == "__main__":
    from pathlib import Path
    from rl_intro.evaluation.parse import parse_experiment_batch_json
    from rl_intro.evaluation.analyze import analyze_experiments

    file_path = Path(__file__).parent.parent.parent / "data/experiment_batch_logs.json"
    batch_experiment_logs = parse_experiment_batch_json(file_path)

    n_rows, n_cols = 4, 10
    analysis = analyze_experiments(batch_experiment_logs, n_rows=n_rows, n_cols=n_cols)
    agents = list(analysis.keys())

    fig, ax = plt.subplots(3, 2, figsize=(12, 10))
    ax = ax.flatten()
    plot_cumulative_reward(analysis, ax[0], interval=(0, 20000))
    plot_average_reward_per_episode(analysis, ax[1], interval=(0, 300))
    plot_final_values(analysis[agents[0]], ax[2])
    plot_final_values(analysis[agents[1]], ax[3])
    plot_state_visit_frequency(analysis[agents[0]], ax[4])
    plot_state_visit_frequency(analysis[agents[1]], ax[5])
    plt.tight_layout()
    plt.show()

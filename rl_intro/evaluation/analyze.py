from typing import Optional
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
from rl_intro.simulation.experiment import ExperimentLog
from rl_intro.evaluation.data_handling import parse_experiment_json, to_dataframe

plt.style.use("dark_background")


def plot_cumulative_reward(df, ax, steps=5000):
    df["cumulative_reward"] = df["reward"].cumsum()
    fig = ax.figure
    ax.set_title("Cumulative Reward Over Time")
    ax.set_xlabel("Steps")
    ax.set_ylabel("Cumulative Reward")
    ax.grid(True, alpha=0.2)
    ax.plot(
        df.index[:steps],
        df["cumulative_reward"][:steps],
        label=f"Cumulative Reward (First {steps} Steps)",
        color="magenta",
    )
    ax.legend()
    plt.tight_layout()
    return fig, ax


def plot_average_reward_per_episode(df, ax, n_episodes=200):
    grouped_episodes = df.groupby("episode")["reward"].sum().reset_index()
    fig = ax.figure
    ax.set_title("Average Reward Per Episode")
    ax.set_xlabel("Episode")
    ax.set_ylabel("Average Reward")
    ax.grid(True, alpha=0.2)
    ax.plot(
        grouped_episodes["episode"][:n_episodes],
        grouped_episodes["reward"][:n_episodes],
        label="Average Reward per Episode",
        color="magenta",
    )
    ax.legend()
    plt.tight_layout()
    return fig, ax


def plot_final_values(final_values, w=10, h=4, ax=None):
    values = np.array(final_values).reshape((h, w))
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure
    cax = ax.imshow(values, cmap="viridis", interpolation="nearest")
    for i in range(h):
        for j in range(w):
            val = values[i, j]
            ax.text(
                j,
                i,
                f"{val:.1f}",
                ha="center",
                va="center",
                color="white" if val < 0.5 else "black",
            )
    ax.set_title("Final Values")
    plt.colorbar(cax, ax=ax, orientation="horizontal")
    plt.tight_layout()
    return fig, ax


def plot_state_visit_frequency(df, w=10, h=4, ax=None):
    state_visit_freq = df.groupby("state").size().reset_index(name="num_visits")
    visit_array = np.zeros((h, w))
    for _, row in state_visit_freq.iterrows():
        state = row["state"]
        visits = row["num_visits"]
        pos = state // w, state % w
        visit_array[pos] = visits
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure
    cax = ax.imshow(visit_array, cmap="viridis", interpolation="nearest")
    plt.colorbar(cax, ax=ax, orientation="horizontal")
    ax.set_title("State Visit Frequency")
    plt.tight_layout()
    return fig, ax


def generate_experiment_report(
    df, final_values=None, w=10, h=4, save_dir: Optional[Path] = None, combined=False
):
    def save_figure(fig, name):
        if save_dir and not combined:
            fig.savefig(save_dir / f"{name}.png")

    if save_dir is not None:
        save_dir.mkdir(parents=True, exist_ok=True)

    if combined:
        fig, axs = plt.subplots(2, 2, figsize=(16, 10))
        ax1, ax2, ax3, ax4 = axs.flatten()
        fig1 = fig2 = fig3 = fig4 = fig
    else:
        fig1, ax1 = plt.subplots(figsize=(12, 5))
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        fig3, ax3 = plt.subplots(figsize=(12, 5))
        fig4, ax4 = (
            plt.subplots(figsize=(10, 5)) if final_values is not None else (None, None)
        )

    plot_cumulative_reward(df, ax1)
    save_figure(fig1, "cumulative_reward")

    plot_average_reward_per_episode(df, ax2)
    save_figure(fig2, "average_reward_per_episode")

    plot_state_visit_frequency(df, w=w, h=h, ax=ax3)
    save_figure(fig3, "state_visit_frequency")

    if final_values is not None:
        plot_final_values(final_values, w=w, h=h, ax=ax4)
        save_figure(fig4, "final_values")

    if combined and save_dir is not None:
        fig1.savefig(save_dir / "combined.png")

    plt.show()


def main():
    experiment_json = Path("experiment_logs.json")
    log = parse_experiment_json(experiment_json)
    df = to_dataframe(log)
    generate_experiment_report(
        df,
        final_values=log.final_values,
        save_dir=Path("data_out"),
        combined=True,
    )


if __name__ == "__main__":
    main()

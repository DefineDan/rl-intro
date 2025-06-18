from rl_intro.simulation.experiment import ExperimentLog, StepLog, ExperimentConfig
from rl_intro.utils.logger import logger
import json
from pathlib import Path
import pandas as pd
import re


def to_dataframe(experiment_log: ExperimentLog) -> pd.DataFrame:
    rows = []
    for step in experiment_log.steps:
        row = {
            "agent": experiment_log.agent,
            "env": experiment_log.env,
            "episode": step.episode,
            "step": step.step,
            "action": step.action,
            "state": step.state,
            "reward": step.reward,
            "terminal": step.terminal,
        }
        rows.append(row)
    return pd.DataFrame(rows)


def to_dataframe_batch(experiment_logs: list[ExperimentLog]) -> pd.DataFrame:
    return pd.concat([to_dataframe(log) for log in experiment_logs], ignore_index=True)


def parse_experiment_data(data: dict) -> ExperimentLog:
    # TODO: maybe use a lib for parsing dataclasses recursively
    logs = [StepLog(**step) for step in data["steps"]]
    exp_config = ExperimentConfig(**data["experiment_config"])
    return ExperimentLog(
        agent=data["agent"],
        env=data["env"],
        experiment_config=exp_config,
        steps=logs,
        final_values=data.get("final_values"),
    )


def parse_experiment_json(json_file: Path) -> ExperimentLog:
    with open(json_file, "r") as f:
        data = json.load(f)
    return parse_experiment_data(data)


def parse_experiment_batch_json(json_file: Path) -> list[ExperimentLog]:
    with open(json_file, "r") as f:
        data = json.load(f)
    return [parse_experiment_data(exp) for exp in data]


def extract_param(df: pd.DataFrame, col: str, param: str, new_col: str) -> pd.DataFrame:
    pattern = re.compile(rf"{param}\s*=\s*([^,\)]+)")

    def extract(s):
        match = pattern.search(s)
        return match.group(1) if match else None

    df[new_col] = df[col].apply(extract)
    return df


# * Example usage
if __name__ == "__main__":
    file_path = Path("experiment_logs.json")
    experiment_log = parse_experiment_json(file_path)

    df = to_dataframe(experiment_log)
    logger.debug(df.head())

    file_path = Path("experiment_batch_logs.json")
    batch_experiment_logs = parse_experiment_batch_json(file_path)
    logger.debug(batch_experiment_logs[0].agent)
    df_batch = to_dataframe_batch(batch_experiment_logs)
    extract_param(df_batch, "agent", "seed", "agent_seed")
    logger.debug(df_batch.head())

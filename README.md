# An Interactive Introduction to Reinforcement Learning


This is an interactive playground for exploring basic concepts of Reinforcement Learning. While there are excellent theoretical explanations, most notably [Reinforcement Learning: An Introduction by Sutton and Barto](http://incompleteideas.net/book/the-book-2nd.html), this project aims to provide some intuition on basic algorithms, parameters and their shortcomings.

[![Demo](docs/demo.gif)](docs/demo.gif)

## Features

- **Interactive Web Interface**: Run RL experiments directly in your browser.
- **Pure Python Core**: Reusable RL algorithms implemented in typed Python.
- **No Backend Required**: Everything runs client-side using WebAssembly.
- **Svelte Frontend**: Compiled, component based frontend using [Svelte](https://svelte.dev/).
- **Static Hosting**: Easily deployable to GitHub Pages or any static host like Vercel or Netlify.

## Architecture

- **Python Package**: Core RL algorithms implemented as a typed Python package [rl_intro](rl_intro/)
- **WebAssembly**: Python code runs in the browser via [Pyodide](https://pyodide.org/)
- **Svelte Frontend**: Fast, compiled frontend using [Svelte](https://svelte.dev/)
- **Static Hosting**: Easily deployable to GitHub Pages or any static host like Vercel or Netlify

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js and npm
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

*Take a look at the [Makefile](Makefile) to see the available commands, which you can also run directly without `make`.*

### Setup

```bash
make setup
```
- Installs Python dependencies using `uv`
- Installs Node.js dependencies for the web interface

### Development

#### Run the Web Interface

```bash
make run-web
```

- Starts the development server and opens the app in your browser

#### Build the Project

```bash
make build
```

- Builds the Python wheel and compiles the web app



## Usage

### Web Interface

Visit the running web application to:
- Configure different RL algorithms (SARSA, Q-Learning, Expected SARSA)
- Set up GridWorld environments with custom parameters
- Run experiments and watch agents learn in real-time
- Visualize learning curves and value functions

### Python scripts and Jupyter Notebooks

Check out the examples in the [examples](examples/) directory:
- [experiment.ipynb](examples/experiment.ipynb) - Basic experiment setup
- [multi_agent_experiment.py](examples/multi_agent_experiment.py) - Compare multiple algorithms
- [multi_seed_experiment.py](examples/multi_seed_experiment.py) - Statistical analysis across multiple runs


```python
from rl_intro.agent.agent_expected_sarsa import AgentExpectedSarsa
from rl_intro.agent.policy import EpsilonGreedyPolicy
from rl_intro.environment.gridworld import GridWorld
from rl_intro.simulation.experiment import Experiment

# Configure agent, environment, and experiment
agent_config = ...
env_config = ...
experiment_config = ...

# Create environment and agent
agent = AgentExpectedSarsa(agent_config, EpsilonGreedyPolicy(policy_config))
env = GridWorld(env_config)
experiment = Experiment(agent, env, experiment_config)

# Run experiment
results = experiment.run()
```

## Environments and Agents Implemented

For now, only tabular methods like Q-Learning and SARSA are implemented in the GridWorld environment. More agents and environments will be added over time.

## Some other (far more advanced) resources

- [Gymnasium (formerly OpenAI Gym)](https://gymnasium.farama.org/): A toolkit for developing and comparing reinforcement learning algorithms.
- [Stable Baselines3](https://stable-baselines3.readthedocs.io/en/master/): A set of reliable implementations of reinforcement learning algorithms in PyTorch.
- [RLlib](https://docs.ray.io/en/latest/rllib/index.html): A library for reinforcement learning that offers both high-level APIs and low-level control.
- [Spinning Up in Deep RL](https://spinningup.openai.com/en/latest/): An educational resource for deep reinforcement learning.
- [CleanRL](https://docs.cleanrl.dev/): A minimalistic implementation of reinforcement learning algorithms.

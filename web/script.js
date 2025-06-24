const StateKind = {
  EMPTY: 0,
  START: 1,
  TERMINAL: 2,
  CLIFF: 3,
  WALL: 4,
};

const AgentType = {
  EXPECTED_SARSA: "expected_sarsa",
  Q_LEARNING: "q_learning",
  SARSA: "sarsa",
};

const stateStyles = {
  [StateKind.EMPTY]: { background: "#f0f0f0", border: "#ccc" },
  [StateKind.START]: { background: "#4caf50", border: "#388e3c" },
  [StateKind.TERMINAL]: { background: "#2196f3", border: "#1976d2" },
  [StateKind.CLIFF]: { background: "#e53935", border: "#b71c1c" },
  [StateKind.WALL]: { background: "#757575", border: "#424242" },
};

const GridMode = {
  CONFIG: "config",
  VALUES: "values",
};

// Global Pyodide instance
let pyodideInstance = null;

// Dynamically load Pyodide and use loadPyodide from the global scope
async function initializePyodide() {
  if (!window.loadPyodide) {
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js";
    script.type = "text/javascript";
    document.head.appendChild(script);
    await new Promise((resolve) => {
      script.onload = resolve;
    });
  }

  if (!pyodideInstance) {
    const loadPyodide = window.loadPyodide;
    console.log("Initializing Pyodide...");
    pyodideInstance = await loadPyodide();

    // Install packages once
    console.log("Installing packages...");
    await pyodideInstance.loadPackage(["micropip"]);
    await pyodideInstance.runPythonAsync(`
      import micropip
      await micropip.install("py/rl_intro-0.1.1-py3-none-any.whl")
      import rl_intro
    `);
    console.log("Pyodide ready!");
  }

  return pyodideInstance;
}

// Initialize Pyodide when the page loads
document.addEventListener("DOMContentLoaded", () => {
  const output = document.getElementById("output");
  output.textContent = "Initializing Python environment...";

  initializePyodide()
    .then(() => {
      output.textContent =
        "Ready! Configure the grid and click Confirm Grid to start.";
    })
    .catch((error) => {
      output.textContent = `Error initializing Python: ${error.message}`;
      console.error(error);
    });
});

window.agentConfig = () => ({
  AgentType, // Make AgentType available to the template
  agentType: AgentType.EXPECTED_SARSA,
  learningRate: 0.3,
  discount: 1.0,
  epsilon: 0.1,
  getConfig() {
    return {
      agent_type: this.agentType,
      learning_rate: this.learningRate,
      discount: this.discount,
      epsilon: this.epsilon,
    };
  },
});

window.gridWorld = () => ({
  GridMode, // Make GridMode available to Alpine.js
  grid: [
    [1, 0, 0, 0, 0, 0, 0, 4, 0, 2],
    [0, 4, 3, 3, 3, 3, 0, 0, 0, 0],
    [0, 4, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
  ],
  selectedState: StateKind.EMPTY,
  agentPos: null,
  gridWidth: 10,
  mode: GridMode.CONFIG,
  agentValues: null,
  isRunning: false,
  stepInterval: null,
  stepDelay: 200, // Default delay in ms
  stateLabels: {
    [StateKind.EMPTY]: "Empty",
    [StateKind.START]: "Start",
    [StateKind.TERMINAL]: "Terminal",
    [StateKind.CLIFF]: "Cliff",
    [StateKind.WALL]: "Wall",
  },

  getCellStyle(kind, row, col) {
    if (this.mode === GridMode.VALUES && this.agentValues) {
      const idx = row * this.gridWidth + col;
      const value = this.agentValues[idx];
      const min = Math.min(...this.agentValues);
      const max = Math.max(...this.agentValues);
      const norm = (value - min) / (max - min || 1);
      const color = d3.interpolateViridis(norm);
      return {
        background: color,
        border: `2px solid ${color}`,
        color: "#fff",
      };
    } else {
      const style = stateStyles[kind] || stateStyles[StateKind.EMPTY];
      return {
        background: style.background,
        border: `2px solid ${style.border}`,
      };
    }
  },

  getCellContent(row, col) {
    if (
      this.agentPos &&
      row === this.agentPos.row &&
      col === this.agentPos.col
    ) {
      return "🤖";
    }
    if (this.mode === GridMode.VALUES && this.agentValues) {
      const idx = row * this.gridWidth + col;
      return this.agentValues[idx].toFixed(1);
    }
    const kind = this.grid[row][col];
    switch (kind) {
      case StateKind.START:
        return "S";
      case StateKind.TERMINAL:
        return "T";
      case StateKind.CLIFF:
        return "C";
      case StateKind.WALL:
        return "W";
      default:
        return "";
    }
  },

  updateCell(row, col) {
    if (this.mode !== GridMode.CONFIG) return;
    this.grid[row][col] = this.selectedState;
  },

  async confirmGrid() {
    const output = document.getElementById("output");
    output.textContent = "Initializing simulation...";

    try {
      const pyodide = await initializePyodide();

      const pyGrid = pyodide.toPy(this.grid);
      pyodide.globals.set("pyGrid", pyGrid);

      let agentConfig = window.agentConfigInstance.getConfig();
      const pyAgentConfig = pyodide.toPy(agentConfig);
      pyodide.globals.set("pyAgentConfig", pyAgentConfig);

      // TODO: Execute once during startup only
      const response = await fetch("/py/simulation.py");
      const code = await response.text();
      await pyodide.runPythonAsync(code);

      await pyodide.runPythonAsync("env = create_gridworld(pyGrid)");
      await pyodide.runPythonAsync(
        "agent = create_agent(pyAgentConfig, env.width * env.height, len(env.action_space))"
      );
      await pyodide.runPythonAsync("init_simulation(env, agent)");

      await pyodide.runPythonAsync("agent_pos = get_current_position(env)");
      this.agentPos = pyodide.globals.get("agent_pos").toJs();

      output.textContent = "Simulation initialized. Ready to step or run.";
    } catch (error) {
      output.textContent = `Error: ${error.message}`;
      console.error(error);
    }
  },

  async step() {
    const output = document.getElementById("output");
    try {
      const pyodide = await initializePyodide();
      await pyodide.runPythonAsync("result = step_simulation()");
      const result = pyodide.globals
        .get("result")
        .toJs({ dict_converter: Object.fromEntries });

      this.agentPos = result.position;
      const stepLog = result.step_log;
      output.textContent = `Episode: ${stepLog.episode}, Step: ${
        stepLog.step
      }, Reward: ${stepLog.reward.toFixed(2)}`;

      if (stepLog.terminal) {
        output.textContent += " (Episode finished)";
      }
    } catch (error) {
      output.textContent = `Error: ${error.message}`;
      console.error(error);
      this.pause();
    }
  },

  run() {
    this.pause();
    this.isRunning = true;
    this.stepInterval = setInterval(() => {
      this.step();
    }, this.stepDelay);
  },

  pause() {
    this.isRunning = false;
    if (this.stepInterval) {
      clearInterval(this.stepInterval);
      this.stepInterval = null;
    }
  },

  reset() {
    this.pause();
    this.mode = GridMode.CONFIG;
    this.agentPos = null;
    this.agentValues = null;
    const output = document.getElementById("output");
    output.textContent =
      "Ready! Configure the grid and click Confirm Grid to start.";
  },

  async runFullAnalysis() {
    const output = document.getElementById("output");
    output.textContent = "Running full analysis...";

    try {
      const pyodide = await initializePyodide();
      pyodide.globals.set("pyGrid", pyodide.toPy(this.grid));
      let agentConfig = window.agentConfigInstance.getConfig();
      pyodide.globals.set("pyAgentConfig", pyodide.toPy(agentConfig));

      await pyodide.runPythonAsync("env = create_gridworld(pyGrid)");
      await pyodide.runPythonAsync(
        "agent = create_agent(pyAgentConfig, env.width * env.height, len(env.action_space))"
      );

      await pyodide.runPythonAsync(
        "experiment_log = run_full_experiment(env, agent)"
      );

      // TODO: move into python
      console.log("Completed Experiment");
      await pyodide.runPythonAsync(
        "analysis = analyze_experiment(experiment_log, env.height, env.width)"
      );
      await pyodide.runPythonAsync(
        "cumulative_reward_json = analysis.cumulative_reward.to_json(orient='split')"
      );
      const cumulativeRewardJson = pyodide.globals.get(
        "cumulative_reward_json"
      );
      const cumulativeReward = JSON.parse(cumulativeRewardJson);
      if (window.plotCumulativeReward) {
        window.plotCumulativeReward(cumulativeReward, "reward-plot");
      }
      // --- End plot ---

      // --- Plot episodic rewards using D3 ---
      await pyodide.runPythonAsync(
        "episodic_rewards_json = analysis.episodic_rewards.to_json(orient='split')"
      );
      const episodicRewardsJson = pyodide.globals.get("episodic_rewards_json");
      const episodicRewards = JSON.parse(episodicRewardsJson);
      if (window.plotEpisodicRewards) {
        window.plotEpisodicRewards(episodicRewards, "episodic-reward-plot");
      }
      // --- End plot ---

      // Update agent position
      await pyodide.runPythonAsync("agent_pos = get_current_position(env)");
      this.agentPos = pyodide.globals.get("agent_pos").toJs();

      await pyodide.runPythonAsync("final_values = agent.get_greedy_values()");
      const finalValues = pyodide.globals.get("final_values").toJs();
      this.agentValues = finalValues;
      console.log("Final values:", finalValues);

      // put in output
      output.textContent = "Analysis complete!";
    } catch (error) {
      output.textContent = `Error: ${error.message}`;
      console.error(error);
    }
  },
});

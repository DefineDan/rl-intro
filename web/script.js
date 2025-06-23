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
      await micropip.install("py/rl_intro-0.1.0-py3-none-any.whl")
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
  grid: [
    [1, 0, 0, 0, 0, 0, 0, 4, 0, 2],
    [0, 4, 3, 3, 3, 3, 0, 0, 0, 0],
    [0, 4, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
  ],
  selectedState: StateKind.EMPTY,
  agentPos: null,
  gridWidth: 10,
  stateLabels: {
    [StateKind.EMPTY]: "Empty",
    [StateKind.START]: "Start",
    [StateKind.TERMINAL]: "Terminal",
    [StateKind.CLIFF]: "Cliff",
    [StateKind.WALL]: "Wall",
  },

  getCellStyle(kind) {
    const style = stateStyles[kind] || stateStyles[StateKind.EMPTY];
    return {
      background: style.background,
      border: `2px solid ${style.border}`,
    };
  },

  getCellContent(row, col) {
    const kind = this.grid[row][col];

    if (
      this.agentPos &&
      row === this.agentPos.row &&
      col === this.agentPos.col
    ) {
      return "🤖";
    }

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
    this.grid[row][col] = this.selectedState;
  },

  async saveGrid() {
    const output = document.getElementById("output");
    output.textContent = "Running simulation...";

    try {
      // Use the existing Pyodide instance
      const pyodide = await initializePyodide();

      // Set the grid variable in Python
      const pyGrid = pyodide.toPy(this.grid);
      pyodide.globals.set("pyGrid", pyGrid);

      let agentConfig = window.agentConfigInstance.getConfig();
      const pyAgentConfig = pyodide.toPy(agentConfig);
      pyodide.globals.set("pyAgentConfig", pyAgentConfig);

      // TODO: Execute once during startup only
      const response = await fetch("/py/simulation.py");
      const code = await response.text();
      await pyodide.runPythonAsync(code); // Defines run_simulation

      await pyodide.runPythonAsync("env = create_gridworld(pyGrid)");
      await pyodide.runPythonAsync(
        "agent = create_agent(pyAgentConfig, env.width * env.height, len(env.action_space))"
      );
      await pyodide.runPythonAsync("experiment_log = run_simulation(env, agent)");

      // Update agent position
      await pyodide.runPythonAsync("agent_pos = get_current_position(env)");
      this.agentPos = pyodide.globals.get("agent_pos").toJs();

      await pyodide.runPythonAsync("final_values = agent.get_greedy_values()");
      const finalValues = pyodide.globals.get("final_values").toJs();
      console.log("Final values:", finalValues);

      // put in output
      output.textContent = "Simulation completed!";
      // Render value heatmap
      renderValueHeatmap(finalValues, this.grid.length, this.grid[0].length);
      
    } catch (error) {
      output.textContent = `Error: ${error.message}`;
      console.error(error);
    }
  },
});

function renderValueHeatmap(flatValues, rows, cols) {
  const matrix = [];
  for (let i = 0; i < rows; i++) {
    matrix.push(flatValues.slice(i * cols, (i + 1) * cols));
  }
  // Reverse for gridworld convention (bottom row last)
  const plotMatrix = matrix.reverse();
  
  // Create text matrix with formatted values
  const textMatrix = plotMatrix.map(row => 
    row.map(val => val.toFixed(2))
  );

  Plotly.newPlot('value-heatmap', [{
    z: plotMatrix,
    type: 'heatmap',
    colorscale: 'Viridis',
    showscale: true,
    hoverongaps: false,
    text: textMatrix,
    texttemplate: '%{text}',
    textfont: {
      size: 14,
      color: 'white'
    },
    showlegend: false
  }], {
    margin: { t: 0, b: 0, l: 0, r: 0 },
    xaxis: { showgrid: false, zeroline: false, showticklabels: false },
    yaxis: { showgrid: false, zeroline: false, showticklabels: false },
  });
}

// Dynamically load Pyodide and use loadPyodide from the global scope
async function loadPyodideScript() {
  if (!window.loadPyodide) {
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js";
    script.type = "text/javascript";
    document.head.appendChild(script);
    await new Promise((resolve) => {
      script.onload = resolve;
    });
  }
  return window.loadPyodide;
}

const StateKind = {
  EMPTY: 0,
  START: 1,
  TERMINAL: 2,
  CLIFF: 3,
  WALL: 4,
};

const stateStyles = {
  [StateKind.EMPTY]: { background: "#f0f0f0", border: "#ccc" },
  [StateKind.START]: { background: "#4caf50", border: "#388e3c" },
  [StateKind.TERMINAL]: { background: "#2196f3", border: "#1976d2" },
  [StateKind.CLIFF]: { background: "#e53935", border: "#b71c1c" },
  [StateKind.WALL]: { background: "#757575", border: "#424242" },
};

// Define the Alpine component
window.gridWorld = () => ({
  grid: [
    [1,0,0,0,0,0,0,4,0,2],
    [0,4,3,3,3,3,0,0,0,0],
    [0,4,0,0,0,0,0,4,0,0],
    [0,0,0,0,0,0,0,4,0,0],
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
    
    if (this.agentPos && row === this.agentPos.row && col === this.agentPos.col) {
      return '🤖';
    }
    
    switch(kind) {
      case StateKind.START: return 'S';
      case StateKind.TERMINAL: return 'T';
      case StateKind.CLIFF: return 'C';
      case StateKind.WALL: return 'W';
      default: return '';
    }
  },

  updateCell(row, col) {
    this.grid[row][col] = this.selectedState;
  },

  async saveGrid() {
    const output = document.getElementById('output');
    output.textContent = 'Saving grid...';
    
    try {
      const loadPyodide = await loadPyodideScript();
      const pyodide = await loadPyodide();
      
      // Install your rl_intro wheel
      await pyodide.loadPackage(["micropip"]);
      await pyodide.runPythonAsync(`
        import micropip
        await micropip.install("py/rl_intro-0.1.0-py3-none-any.whl")
      `);

      // Your Python script
      const code = `
from rl_intro.agent.core import AgentConfig
from rl_intro.agent.agent_expected_sarsa import AgentExpectedSarsa
from rl_intro.environment.gridworld import GridWorld, GridWorldConfig
from rl_intro.agent.policy import EpsilonGreedyPolicy, EpsilonGreedyConfig
from rl_intro.simulation.experiment import Experiment, ExperimentConfig
from rl_intro.utils.visualize import grid_str

grid = ${JSON.stringify(this.grid)}
w, h = len(grid[0]), len(grid)

# Find start and terminal states
start_states = []
terminal_states = []
cliff_states = []
wall_states = []

for i in range(h):
    for j in range(w):
        state = i * w + j
        cell = grid[i][j]
        if cell == 1:  # Start
            start_states.append(state)
        elif cell == 2:  # Terminal
            terminal_states.append(state)
        elif cell == 3:  # Cliff
            cliff_states.append(state)
        elif cell == 4:  # Wall
            wall_states.append(state)

env_config = GridWorldConfig(
    width=w,
    height=h,
    start_states=start_states,
    terminal_states=terminal_states,
    cliff_states=cliff_states,
    wall_states=wall_states,
    random_seed=42,
)
env = GridWorld(env_config)

agent_config = AgentConfig(
    n_states=w * h,
    n_actions=len(env.action_space),
    random_seed=42,
    learning_rate=0.3,
    discount=1.0,
)
agent = AgentExpectedSarsa(
    agent_config, EpsilonGreedyPolicy(EpsilonGreedyConfig(epsilon=0.1))
)

experiment_config = ExperimentConfig(n_episodes=1000, max_steps=200)
experiment = Experiment(agent, env, experiment_config)

log = []

log.append("Before training:")
log.append(env.to_str())
log.append(grid_str(agent.get_greedy_actions(), w, h))
log.append(grid_str(agent.get_greedy_values(), w, h))

experiment.run()

log.append("After training:")
log.append(env.to_str())
log.append(grid_str(agent.get_greedy_actions(), w, h))
log.append(grid_str(agent.get_greedy_values(), w, h))

output = "\\n\\n".join(log)
`;

      const result = await pyodide.runPythonAsync(code + "\noutput");
      output.textContent = result;

      // Access Python objects from JS
      const agent = pyodide.globals.get("agent");
      const env = pyodide.globals.get("env");
      const position = env.get_position(env.state).toJs();
      this.agentPos = { row: position[0][0], col: position[1][0] };
      
    } catch (error) {
      output.textContent = `Error: ${error.message}`;
      console.error(error);
    }
  }
});

export const StateKind = {
  EMPTY: 0,
  START: 1,
  TERMINAL: 2,
  CLIFF: 3,
  WALL: 4,
};

export const stateStyles = {
  [StateKind.EMPTY]: { background: "#f0f0f0", border: "#ccc" },
  [StateKind.START]: { background: "#4caf50", border: "#388e3c" },
  [StateKind.TERMINAL]: { background: "#2196f3", border: "#1976d2" },
  [StateKind.CLIFF]: { background: "#e53935", border: "#b71c1c" },
  [StateKind.WALL]: { background: "#757575", border: "#424242" },
};

export const stateLabels = {
  [StateKind.EMPTY]: "Empty",
  [StateKind.START]: "Start",
  [StateKind.TERMINAL]: "Terminal",
  [StateKind.CLIFF]: "Cliff",
  [StateKind.WALL]: "Wall",
};

export const GridMode = {
  CONFIG: "config",
  VALUES: "values",
};

export const initialGrid = [
  [1, 0, 0, 0, 0, 0, 0, 4, 0, 2],
  [0, 4, 3, 3, 3, 3, 0, 0, 0, 0],
  [0, 4, 0, 0, 0, 0, 0, 4, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
];

export const AgentType = {
  EXPECTED_SARSA: "expected_sarsa",
  Q_LEARNING: "q_learning",
  SARSA: "sarsa",
}; 
export const StateKind = {
  EMPTY: 0,
  START: 1,
  TERMINAL: 2,
  CLIFF: 3,
  WALL: 4,
};

export const stateBootstrapClasses = {
  [StateKind.EMPTY]: "btn-dark",
  [StateKind.START]: "btn-info",
  [StateKind.TERMINAL]: "btn-success",
  [StateKind.CLIFF]: "btn-danger",
  [StateKind.WALL]: "btn-primary",
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
  VIEW: "view",
  VALUES: "values",
  VISITS: "visits",
};

export const initialGrid = [
  [1, 0, 0, 0, 0, 0, 0, 4, 0, 2],
  [0, 4, 3, 3, 3, 3, 0, 0, 0, 0],
  [0, 4, 0, 0, 0, 0, 0, 4, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
];

export const AgentType = {
  EXPECTED_SARSA: "expected_sarsa",
  Q_LEARNING: "q_learning",
  SARSA: "sarsa",
};

//   --bs-primary: #6f42c1;
//   --bs-secondary: #ea39b8;
//   --bs-success: #3cf281;
//   --bs-info: #1ba2f6;
//   --bs-warning: #ffc107;
//   --bs-danger: #e44c55;
//   --bs-light: #44d9e8;
//   --bs-dark: #170229;

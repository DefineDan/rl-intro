import { getPyodide } from './pyodide.js';

export async function initializeSimulation(grid, agentConfig) {
  const pyodide = await getPyodide();
  await pyodide.runPythonAsync("reset_globals()");
  const pyGrid = pyodide.toPy(grid);
  pyodide.globals.set("pyGrid", pyGrid);
  await pyodide.runPythonAsync(`create_gridworld(pyGrid)`);
  const pyAgentConfig = pyodide.toPy(agentConfig);
  pyodide.globals.set("pyAgentConfig", pyAgentConfig);
  await pyodide.runPythonAsync(`create_agent(pyAgentConfig)`);
  await pyodide.runPythonAsync(`create_experiment()`);
}

export async function getCurrentPosition() {
  const pyodide = await getPyodide();
  const position = await pyodide.runPythonAsync("get_current_position()");
  return position.toJs();
}

export async function stepExperiment() {
  const pyodide = await getPyodide();
  const step_result = await pyodide.runPythonAsync("step_experiment()");
  return step_result.toJs({dict_converter: Object.fromEntries});
}

export async function runFullExperiment() {
  const pyodide = await getPyodide();
  await pyodide.runPythonAsync("run_full_experiment()");
}

export async function analyzeExperimentLogs() {
  const pyodide = await getPyodide();
  const analysis = await pyodide.runPythonAsync("analyze_experiment_logs()");
  return analysis.toJs({dict_converter: Object.fromEntries});
} 
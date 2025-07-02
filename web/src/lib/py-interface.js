import { loadPyodide } from "pyodide";
import { base } from "$app/paths";

// TODO: put paths into a config file

let pyodidePromise = null;

export async function getPyodide() {
  if (!pyodidePromise) {
    pyodidePromise = (async () => {
      console.log("Initializing Pyodide...");
      const pyodide = await loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/",
      });
      // Install packages once
      console.log("Installing rl_intro packages...");
      await pyodide.loadPackage(["micropip"]);
      await pyodide.runPythonAsync(`
                import micropip
                await micropip.install("${base}/py/rl_intro-0.1.1-py3-none-any.whl")
                import rl_intro
            `);
      const response = await fetch(`${base}/py/rl_intro_wrapper.py`);
      const code = await response.text();
      await pyodide.runPythonAsync(code);
      console.log("Pyodide ready to go!");
      return pyodide;
    })();
  }
  return pyodidePromise;
}

export function getAgentConfigForPython(agentConfig) {
  return {
    agent_type: agentConfig.agentType,
    learning_rate: agentConfig.learningRate,
    discount: agentConfig.discount,
    epsilon: agentConfig.epsilon,
  };
}

export function getExperimentConfigForPython(experimentConfig) {
  return {
    n_episodes: experimentConfig.nEpisodes,
    max_steps: experimentConfig.maxSteps,
  };
}

export async function initializeSimulation(
  simId,
  grid,
  agentConfig,
  experimentConfig
) {
  const pyodide = await getPyodide();
  const pyGridConfig = pyodide.toPy(grid);
  pyodide.globals.set("pyGridConfig", pyGridConfig);
  const pyAgentConfig = pyodide.toPy(getAgentConfigForPython(agentConfig));
  pyodide.globals.set("pyAgentConfig", pyAgentConfig);
  const pyExperimentConfig = pyodide.toPy(
    getExperimentConfigForPython(experimentConfig)
  );
  pyodide.globals.set("pyExperimentConfig", pyExperimentConfig);
  await pyodide.runPythonAsync(
    `create_simulation('${simId}', pyGridConfig, pyAgentConfig, pyExperimentConfig)`
  );
}

export async function getCurrentPosition(simId) {
  const pyodide = await getPyodide();
  const position = await pyodide.runPythonAsync(
    `get_current_position('${simId}')`
  );
  return position.toJs();
}

export async function stepExperiment(simId) {
  const pyodide = await getPyodide();
  const step_result = await pyodide.runPythonAsync(
    `step_experiment('${simId}')`
  );
  return step_result.toJs({ dict_converter: Object.fromEntries });
}

export async function runFullExperiment(simId) {
  const pyodide = await getPyodide();
  await pyodide.runPythonAsync(`run_full_experiment('${simId}')`);
}

export async function analyzeExperimentLogs(simId) {
  const pyodide = await getPyodide();
  const analysis = await pyodide.runPythonAsync(
    `analyze_experiment_logs('${simId}')`
  );
  return analysis.toJs({ dict_converter: Object.fromEntries });
}

export async function resetSimulation(simId) {
  const pyodide = await getPyodide();
  await pyodide.runPythonAsync(`reset_simulation('${simId}')`);
}

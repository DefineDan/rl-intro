import { loadPyodide } from 'pyodide';

let pyodidePromise = null;

export async function getPyodide() {
    if (!pyodidePromise) {
        pyodidePromise = (async () => {
            console.log('Initializing Pyodide...');
            const pyodide = await loadPyodide({
                indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/',
            });

            // Install packages once
            console.log('Installing packages...');
            await pyodide.loadPackage(['micropip']);
            // The wheel path is relative to the built app's root
            await pyodide.runPythonAsync(`
        import micropip
        await micropip.install("/py/rl_intro-0.1.1-py3-none-any.whl")
        import rl_intro
      `);
            const response = await fetch('/py/simulation.py');
            const code = await response.text();
            await pyodide.runPythonAsync(code);
            console.log('Pyodide ready to go!');
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
        epsilon: agentConfig.epsilon
    };
}

export function getExperimentConfigForPython(experimentConfig) {
    return {
        n_episodes: experimentConfig.nEpisodes,
        max_steps: experimentConfig.maxSteps
    };
}

export async function initializeSimulation(grid, agentConfig, experimentConfig) {
    const pyodide = await getPyodide();
    await pyodide.runPythonAsync('reset_globals()');

    const pyGridConfig = pyodide.toPy(grid);
    pyodide.globals.set('pyGridConfig', pyGridConfig);
    await pyodide.runPythonAsync(`create_gridworld(pyGridConfig)`);

    const pyAgentConfig = pyodide.toPy(getAgentConfigForPython(agentConfig));
    pyodide.globals.set('pyAgentConfig', pyAgentConfig);
    await pyodide.runPythonAsync(`create_agent(pyAgentConfig)`);

    const pyExperimentConfig = pyodide.toPy(getExperimentConfigForPython(experimentConfig));
    pyodide.globals.set('pyExperimentConfig', pyExperimentConfig);
    await pyodide.runPythonAsync(`create_experiment(pyExperimentConfig)`);
}

export async function getCurrentPosition() {
    const pyodide = await getPyodide();
    const position = await pyodide.runPythonAsync('get_current_position()');
    return position.toJs();
}

export async function stepExperiment() {
    const pyodide = await getPyodide();
    const step_result = await pyodide.runPythonAsync('step_experiment()');
    return step_result.toJs({ dict_converter: Object.fromEntries });
}

export async function runFullExperiment() {
    const pyodide = await getPyodide();
    await pyodide.runPythonAsync('run_full_experiment()');
}

export async function analyzeExperimentLogs() {
    const pyodide = await getPyodide();
    const analysis = await pyodide.runPythonAsync('analyze_experiment_logs()');
    return analysis.toJs({ dict_converter: Object.fromEntries });
} 
// Dynamically load Pyodide and use loadPyodide from the global scope
async function loadPyodideScript() {
  if (!window.loadPyodide) {
    const script = document.createElement('script');
    script.src = "https://cdn.jsdelivr.net/pyodide/v0.27.7/full/pyodide.js";
    script.type = "text/javascript";
    document.head.appendChild(script);
    await new Promise((resolve) => {
      script.onload = resolve;
    });
  }
  return window.loadPyodide;
}

async function main() {
  console.log("STARTING UP!!!");
  const loadPyodide = await loadPyodideScript();
  const pyodide = await loadPyodide();
  const output = document.getElementById("output");

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

w, h = 10, 4

env_config = GridWorldConfig(
    width=w,
    height=h,
    start_states=[0],
    terminal_states=[39],
    cliff_states=[4, 24, 5, 25],
    wall_states=[2, 12, 22, 17, 27, 37],
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
  // Example: get greedy actions as JS array
  const greedyActions = agent.get_greedy_actions().toJs();
  console.log("Greedy actions (JS array):", greedyActions);
  console.log(agent);
  console.log(env);
  // Clean up if needed: agent.destroy();
  console.log("Agent destroyed.");
}

main();
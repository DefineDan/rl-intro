<script>
  import Grid from "./Grid.svelte";
  import { GridMode, initialGrid, StateKind, AgentType } from "./constants.js";
  import AgentConfig from "./ConfigAgent.svelte";
  import ExperimentConfig from "./ConfigExperiment.svelte";
  import * as pyInterface from "./py-interface.js";
  import { onMount } from "svelte";
  import ModeToggle from "./ControlsGrid.svelte";
  import GridControls from "./ConfigGrid.svelte";
  import SimulationControls from "./ControlsSimulation.svelte";
  import SpeedControl from "./ControlsSpeed.svelte";
  import { faCheck } from "@fortawesome/free-solid-svg-icons";
  import { FontAwesomeIcon } from "@fortawesome/svelte-fontawesome";
  import { v4 as uuidv4 } from "uuid";
  import PlotReward from "./PlotReward.svelte";

  let { agentType = AgentType.Q_LEARNING } = $props();

  const simId = uuidv4();

  let grid = $state(JSON.parse(JSON.stringify(initialGrid)));
  let mode = $state(GridMode.CONFIG);
  let selectedStateKind = $state(StateKind.EMPTY);
  let agentPos = $state(null);
  let agentValues = $state(null);
  let agentVisits = $state(null);
  let agentConfig = $state({
    agentType: agentType,
    learningRate: 0.2,
    discount: 1.0,
    epsilon: 0.1,
  });
  let experimentConfig = $state({
    nEpisodes: 500,
    maxSteps: 200,
  });
  let output = $state("Loading...");
  let isRunning = $state(false);
  let stepInterval = $state(null);
  let stepDelay = $state(150);
  let isInitialized = $state(false);
  let cumulativeReward = $state(null);
  let episodicRewards = $state(null);
  let episodeNum = $state(0);

  let gridWidth = $derived(grid[0].length);
  let gridHeight = $derived(grid.length);

  onMount(() => {
    output = "Initializing Python environment...";
    pyInterface
      .getPyodide()
      .then(() => {
        output = "Ready! Configure the grid and click Confirm Grid to start.";
      })
      .catch((error) => {
        output = `Error initializing Python: ${error.message}`;
        console.error(error);
      });
  });

  function updateCellKind(row, col) {
    grid[row][col] = selectedStateKind;
  }

  async function confirmGrid() {
    output = "Initializing simulation...";
    mode = GridMode.VIEW;
    try {
      await pyInterface.initializeSimulation(
        simId,
        grid,
        agentConfig,
        experimentConfig
      );
      agentPos = await pyInterface.getCurrentPosition(simId);
      output = "Simulation initialized. Ready to step or run.";
      isInitialized = true;
    } catch (error) {
      output = `Error: ${error.message}`;
      console.error(error);
    }
  }

  async function step() {
    try {
      const stepResult = await pyInterface.stepExperiment(simId);
      agentPos = stepResult.position;
      agentValues = stepResult.values;
      episodeNum = stepResult.step_log.episode;
      output = `Episode: ${episodeNum}, Step: ${
        stepResult.step_log.step
      }, Reward: ${stepResult.step_log.reward.toFixed(2)}`;

      if (stepResult.step_log.terminal) {
        output += " (Episode finished)";
        const results = await pyInterface.analyzeExperimentLogs(simId);
        cumulativeReward = JSON.parse(results.cumulative_reward);
        episodicRewards = JSON.parse(results.episodic_rewards);
        agentVisits = results.visits;
        if (episodeNum == experimentConfig.nEpisodes) {
          pause();
        }
      }
    } catch (error) {
      output = `Error: ${error.message}`;
      console.error(error);
      pause();
    }
  }

  function run() {
    pause();
    isRunning = true;
    stepInterval = setInterval(step, stepDelay);
  }

  function pause() {
    isRunning = false;
    if (stepInterval) {
      clearInterval(stepInterval);
      stepInterval = null;
    }
  }

  async function reset() {
    pause();
    mode = GridMode.CONFIG;
    episodeNum = 0;
    agentPos = null;
    agentValues = null;
    agentVisits = null;
    cumulativeReward = null;
    episodicRewards = null;
    isInitialized = false;
    await pyInterface.resetSimulation(simId);
    output =
      "Ready! Configure the grid and agent, then click Confirm to start.";
  }

  async function runFullAnalysis() {
    output = "Running full analysis...";
    try {
      pause();
      await pyInterface.initializeSimulation(
        simId,
        grid,
        agentConfig,
        experimentConfig
      );
      await pyInterface.runFullExperiment(simId);

      const results = await pyInterface.analyzeExperimentLogs(simId);
      cumulativeReward = JSON.parse(results.cumulative_reward);
      episodicRewards = JSON.parse(results.episodic_rewards);
      agentValues = results.values;
      agentVisits = results.visits;

      agentPos = await pyInterface.getCurrentPosition(simId);
      episodeNum = experimentConfig.nEpisodes;
      output = `Experiment complete!`;
    } catch (error) {
      output = `Error: ${error.message}`;
      console.error(error);
    }
  }

  function addRow() {
    const newRow = Array(gridWidth).fill(StateKind.EMPTY);
    grid = [...grid, newRow];
  }

  function removeRow() {
    if (grid.length > 1) {
      grid = grid.slice(0, -1);
    }
  }

  function addColumn() {
    grid = grid.map((row) => [...row, StateKind.EMPTY]);
  }

  function removeColumn() {
    if (grid[0].length > 1) {
      grid = grid.map((row) => row.slice(0, -1));
    }
  }
</script>

<div class="card border-dark sim-container">
  <pre class="alert alert-dismissible alert-info">{output}</pre>
  <div class="sim-layout">
    <div class="sim-left">
      <div class="grid-center">
        <ModeToggle
          {mode}
          {GridMode}
          {agentValues}
          {agentVisits}
          setMode={(newMode) => (mode = newMode)}
        />
        <Grid
          {grid}
          {mode}
          {agentPos}
          {agentValues}
          {agentVisits}
          onclick={updateCellKind}
          editable={mode === GridMode.CONFIG}
        />
      </div>
    </div>
    <div class="sim-right">
      <AgentConfig bind:config={agentConfig} />
      <ExperimentConfig bind:config={experimentConfig} />
    </div>
  </div>
  {#if mode === GridMode.CONFIG}
    <div class="config-controls-row">
      <GridControls
        {selectedStateKind}
        setSelectedState={(state) => (selectedStateKind = state)}
        {addRow}
        {removeRow}
        {addColumn}
        {removeColumn}
      />
      <button class="btn btn-success btn-config-confirm" onclick={confirmGrid}
        ><FontAwesomeIcon icon={faCheck} /> Confirm Configuration</button
      >
    </div>
  {/if}
  {#if cumulativeReward && episodicRewards}
    <PlotReward {cumulativeReward} {episodicRewards} {simId} />
  {/if}
  {#if mode !== GridMode.CONFIG && isInitialized}
    <div class="progress mb-3">
      <div
        class="progress-bar progress-bar-animated"
        role="progressbar"
        aria-valuenow={episodeNum}
        aria-valuemin="0"
        aria-valuemax={experimentConfig.nEpisodes}
        style={"width: " +
          (episodeNum / experimentConfig.nEpisodes) * 100 +
          "%;"}
      ></div>
    </div>
    <div class="sim-controls-box alert alert-primary">
      <SimulationControls {step} {run} {pause} {reset} {runFullAnalysis} />
      <SpeedControl
        {stepDelay}
        setStepDelay={(val) => (stepDelay = val)}
        {isRunning}
        {run}
      />
    </div>
  {/if}
</div>

<style>
  .sim-layout {
    display: flex;
    flex-direction: row;
    align-items: flex-start;
    justify-content: stretch;
    gap: 50px;
  }
  .sim-left {
    flex: 1 1 0%;
    display: flex;
    flex-direction: column;
    align-items: stretch;
  }
  .grid-center {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    width: 100%;
  }
  .sim-right {
    padding: 5px;
    min-width: 260px;
    max-width: 340px;
  }
  pre {
    margin-bottom: 2rem;
    padding: 12px;
    font-family: "Menlo", "Consolas", "Liberation Mono", "Courier New",
      monospace;
    background: #222;
    color: #0dc814;
  }
  .sim-container {
    padding: 1rem;
    margin-top: 1rem;
    margin-bottom: 1rem;
  }

  .config-controls-row button {
    margin-top: 0;
    margin: 0.1em;
    margin-top: 0.5em;
  }
  .config-controls-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 1rem;
    margin-top: 0.5em;
  }
  .btn-config-confirm {
    flex: 1;
  }
  .sim-controls-box {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 1rem auto 0 auto;
    border-radius: 1rem !important;
    max-width: 100%;
  }
</style>

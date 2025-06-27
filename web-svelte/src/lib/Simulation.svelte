<script>
	import Grid from './Grid.svelte';
	import { GridMode, initialGrid, StateKind, AgentType } from './constants.js';
	import AgentConfig from './AgentConfig.svelte';
	import * as pyInterface from './py-interface.js';
	import { onMount } from 'svelte';
	import ModeToggle from './ModeToggle.svelte';
	import GridControls from './GridControls.svelte';
	import SimulationControls from './SimulationControls.svelte';
	import SpeedControl from './SpeedControl.svelte';
	import { faCheck } from '@fortawesome/free-solid-svg-icons';
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
	import Plots from './Plots.svelte';

	let grid = $state(JSON.parse(JSON.stringify(initialGrid)));
	let mode = $state(GridMode.CONFIG);
	let selectedStateKind = $state(StateKind.EMPTY);
	let agentPos = $state(null);
	let agentValues = $state(null);
	let agentVisits = $state(null);
	let agentConfig = $state({
		agentType: AgentType.EXPECTED_SARSA,
		learningRate: 0.3,
		discount: 1.0,
		epsilon: 0.1
	});
	let output = $state('Loading...');
	let isRunning = $state(false);
	let stepInterval = $state(null);
	let stepDelay = $state(205);
	let isInitialized = $state(false);
	let gridWidth = $state(initialGrid[0].length);
	let gridHeight = $state(initialGrid.length);
	let cumulativeReward = $state(null);
	let episodicRewards = $state(null);

	onMount(() => {
		output = 'Initializing Python environment...';
		pyInterface.getPyodide()
			.then(() => {
				output = 'Ready! Configure the grid and click Confirm Grid to start.';
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
		output = 'Initializing simulation...';
		mode = GridMode.VIEW
		try {
			const agent_config_for_python = {
				agent_type: agentConfig.agentType,
				learning_rate: agentConfig.learningRate,
				discount: agentConfig.discount,
				epsilon: agentConfig.epsilon
			};
			await pyInterface.initializeSimulation(grid, agent_config_for_python);
			agentPos = await pyInterface.getCurrentPosition();
			output = 'Simulation initialized. Ready to step or run.';
			isInitialized = true;
		} catch (error) {
			output = `Error: ${error.message}`;
			console.error(error);
		}
	}

	async function step() {
		try {
			const stepResult = await pyInterface.stepExperiment();
			agentPos = stepResult.position;
			agentValues = stepResult.values;
			output = `Episode: ${stepResult.step_log.episode}, Step: ${
				stepResult.step_log.step
			}, Reward: ${stepResult.step_log.reward.toFixed(2)}`;

			if (stepResult.step_log.terminal) {
				output += ' (Episode finished)';
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

	function reset() {
		pause();
		mode = GridMode.CONFIG;
		agentPos = null;
		agentValues = null;
		output = 'Ready! Configure the grid and click Confirm Configuration to start.';
		isInitialized = false;
		cumulativeReward = null;
		episodicRewards = null;
	}

	async function runFullAnalysis() {
		output = 'Running full analysis...';
		try {
			pause();
			const agent_config_for_python = {
				agent_type: agentConfig.agentType,
				learning_rate: agentConfig.learningRate,
				discount: agentConfig.discount,
				epsilon: agentConfig.epsilon
			};
			await pyInterface.initializeSimulation(grid, agent_config_for_python);
			await pyInterface.runFullExperiment();
			const results = await pyInterface.analyzeExperimentLogs();

			cumulativeReward = JSON.parse(results.cumulative_reward);
			episodicRewards = JSON.parse(results.episodic_rewards);

			agentPos = await pyInterface.getCurrentPosition();
			agentValues = results.values;
			output = 'Experiment Analysis complete!';
		} catch (error) {
			output = `Error: ${error.message}`;
			console.error(error);
		}
	}

	function addRow() {
		const newRow = Array(gridWidth).fill(StateKind.EMPTY);
		grid = [...grid, newRow];
		gridHeight = grid.length;
	}

	function removeRow() {
		if (grid.length > 1) {
			grid = grid.slice(0, -1);
			gridHeight = grid.length;
		}
	}

	function addColumn() {
		grid = grid.map(row => [...row, StateKind.EMPTY]);
		gridWidth = grid[0].length;
	}

	function removeColumn() {
		if (grid[0].length > 1) {
			grid = grid.map(row => row.slice(0, -1));
			gridWidth = grid[0].length;
		}
	}
</script>

<div class="card border-dark sim-container">
	<pre class="alert alert-dismissible alert-info">{output}</pre>
	<div class="sim-layout">
		<div class="sim-left">
			<ModeToggle {mode} {GridMode} {agentValues} setMode={newMode => mode = newMode} />
			<Grid {grid} {mode} {agentPos} {agentValues} onclick={updateCellKind} editable={mode === GridMode.CONFIG} />
		</div>
		<div class="sim-right">
			<AgentConfig bind:config={agentConfig} />
		</div>
	</div>
	{#if mode === GridMode.CONFIG}
		<div class="config-controls-row">
			<GridControls {selectedStateKind} setSelectedState={state => selectedStateKind = state}
				addRow={addRow} removeRow={removeRow} addColumn={addColumn} removeColumn={removeColumn} />
			<button class="btn btn-success btn-config-confirm" onclick={confirmGrid}><FontAwesomeIcon icon={faCheck} /> Confirm Configuration</button>
		</div>
	{/if}
	<div class="sim-controls-row">
		{#if mode !== GridMode.CONFIG && isInitialized}
			<SimulationControls {step} {run} {pause} {reset} {runFullAnalysis} />
			<SpeedControl {stepDelay} setStepDelay={val => stepDelay = val} {isRunning} {run} />
		{/if}
	</div>
	{#if cumulativeReward && episodicRewards}
		<Plots {cumulativeReward} {episodicRewards} />
	{/if}
</div>

<style>
	.sim-layout {
		display: flex;
		flex-direction: row;
		align-items: flex-start;
		justify-content: space-between;
		gap: 50px;
	}
	.sim-right {
		padding: 5px;
		min-width: 260px;
	}
	pre {
		margin-bottom: 2rem;
		padding: 12px;
		font-family: 'Menlo', 'Consolas', 'Liberation Mono', 'Courier New', monospace;
		background: #222;
		color: #0dc814;
	}
	.sim-container {
		padding: 1rem;
	}
	.sim-controls-row {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 1.5rem;
		/* margin-top: 1.5rem; */
	}

	.config-controls-row button{
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
	.btn-config-confirm{
		flex: 1;
	}
</style> 
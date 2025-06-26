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
	import { plotCumulativeReward, plotEpisodicRewards } from './plot.js';

	let grid = $state(JSON.parse(JSON.stringify(initialGrid)));
	let mode = $state(GridMode.CONFIG);
	let selectedStateKind = $state(StateKind.EMPTY);
	let agentPos = $state(null);
	let agentValues = $state(null);
	let agentConfig = $state({
		agentType: AgentType.EXPECTED_SARSA,
		learningRate: 0.3,
		discount: 1.0,
		epsilon: 0.1
	});
	let output = $state('Loading...');
	let isRunning = $state(false);
	let stepInterval = $state(null);
	let stepDelay = $state(200);

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
		output = 'Ready! Configure the grid and click Confirm Grid to start.';
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

			const cumulativeReward = JSON.parse(results.cumulative_reward);
			const episodicRewards = JSON.parse(results.episodic_rewards);

			plotCumulativeReward(cumulativeReward, "reward-plot");
			plotEpisodicRewards(episodicRewards, "episodic-reward-plot");

			agentPos = await pyInterface.getCurrentPosition();
			agentValues = results.values;

			output = 'Analysis complete!';
		} catch (error) {
			output = `Error: ${error.message}`;
			console.error(error);
		}
	}
</script>

<ModeToggle {mode} {GridMode} {agentValues} setMode={newMode => mode = newMode} />
<div class="sim-layout">
	<div class="sim-left">
		<Grid {grid} {mode} {agentPos} {agentValues} onclick={updateCellKind} />
		{#if mode === GridMode.CONFIG}
			<GridControls {selectedStateKind} setSelectedState={state => selectedStateKind = state} />
		{/if}
	</div>
	<div class="sim-right">
		<AgentConfig bind:config={agentConfig} />
	</div>
</div>
<SimulationControls {confirmGrid} {step} {run} {pause} {reset} />
<SpeedControl {stepDelay} setStepDelay={val => stepDelay = val} {isRunning} {run} />
<button onclick={runFullAnalysis}>Run Full Analysis</button>
<pre>{output}</pre>
<div id="reward-plot"></div>
<div id="episodic-reward-plot"></div>

<style>
	.sim-layout {
		display: flex;
		flex-direction: row;
		align-items: flex-start;
		gap: 50px;
	}
	.sim-right {
		min-width: 260px;
	}
	pre {
		margin-top: 12px;
		padding: 12px;
		background: #f0f0f0;
		border: 1px solid #ccc;
		border-radius: 4px;
		white-space: pre-wrap;
	}
</style> 
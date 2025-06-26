<script>
	import Grid from '$lib/Grid.svelte';
	import { GridMode, initialGrid, stateLabels, StateKind, AgentType } from '$lib/constants.js';
	import AgentConfig from '$lib/AgentConfig.svelte';
	import * as pyInterface from '$lib/py-interface.js';
	import { onMount } from 'svelte';

	let grid = $state(JSON.parse(JSON.stringify(initialGrid)));
	let mode = $state(GridMode.CONFIG);
	let selectedState = $state(StateKind.EMPTY);
	let agentPos = $state(null);
	let agentValues = $state(null);
	let config = $state({
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

	function updateCell(row, col) {
		grid[row][col] = selectedState;
	}

	async function confirmGrid() {
		output = 'Initializing simulation...';
		try {
			const agent_config_for_python = {
				agent_type: config.agentType,
				learning_rate: config.learningRate,
				discount: config.discount,
				epsilon: config.epsilon
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
</script>

<h1>RL Intro in Svelte</h1>

<div class="mode-toggle" style="margin-bottom: 12px; display: flex; gap: 8px;">
	<button class:active={mode === GridMode.CONFIG} onclick={() => (mode = GridMode.CONFIG)}>
		Grid Config
	</button>
	<button
		class:active={mode === GridMode.VALUES}
		onclick={() => (mode = GridMode.VALUES)}
		disabled={!agentValues}
	>
		Agent Values
	</button>
</div>

<Grid {grid} {mode} {agentPos} {agentValues} onclick={updateCell} />

{#if mode === GridMode.CONFIG}
	<div class="controls">
		{#each Object.entries(stateLabels) as [state, label]}
			<button
				class:active={selectedState === parseInt(state)}
				onclick={() => (selectedState = parseInt(state))}
			>
				{label}
			</button>
		{/each}
	</div>
{/if}

<AgentConfig bind:config />

<div class="simulation-controls">
	<button onclick={confirmGrid}>Confirm Grid</button>
	<button onclick={step}>Step</button>
	<button onclick={run}>Run</button>
	<button onclick={pause}>Pause</button>
	<button onclick={reset}>Reset</button>
	<!-- <button onclick={runFullAnalysis}>Run Full Analysis</button> -->
</div>

<div class="speed-control">
	<label for="speed-slider">Speed</label>
	<input
		id="speed-slider"
		type="range"
		min="10"
		max="500"
		step="10"
		bind:value={stepDelay}
		oninput={() => {
			if (isRunning) run();
		}}
	/>
	<span>{stepDelay} ms</span>
</div>

<pre>{output}</pre>

<style>
	.active {
		background-color: #007bff;
		color: white;
	}

	.simulation-controls {
		margin-top: 12px;
		display: flex;
		gap: 8px;
	}

	.speed-control {
		margin-top: 12px;
		display: flex;
		align-items: center;
		gap: 8px;
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

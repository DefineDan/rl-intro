<script>
	let { stepDelay, setStepDelay, isRunning, run } = $props();
</script>

<div class="speed-control">
	<label for="speed-slider">Speed</label>
	<input
		id="speed-slider"
		type="range"
		min="5"
		max="500"
		step="10"
		bind:value={stepDelay}
		oninput={() => {
			setStepDelay(stepDelay);
			if (isRunning) run();
		}}
	/>
	<span>{stepDelay} ms</span>
</div>

<style>
	.speed-control {
		margin-top: 12px;
		display: flex;
		align-items: center;
		gap: 8px;
	}
</style> 
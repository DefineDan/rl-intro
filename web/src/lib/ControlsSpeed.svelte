<script>
	let { stepDelay, setStepDelay, isRunning, run } = $props();

	function stepDelayToSliderValue(delay) {
		return Math.round(1 + ((500 - delay) * 99) / 499);
	}

	function sliderValueToStepDelay(value) {
		return Math.round(500 - ((value - 1) * 499) / 99);
	}

	let sliderValue = $state(stepDelayToSliderValue(stepDelay));

	function handleSliderInput(e) {
		const value = +e.target.value;
		const delay = sliderValueToStepDelay(value);
		setStepDelay(delay);
		if (isRunning) run();
	}
</script>

<div class="speed-control">
	<label for="speed-slider">Speed</label>
	<input
		id="speed-slider"
		class="form-range"
		type="range"
		min="1"
		max="100"
		step="1"
		bind:value={sliderValue}
		oninput={handleSliderInput}
	/>
	<span>{sliderValue}%</span>
</div>

<style>
	.speed-control {
		margin-top: 0.5em;
		display: flex;
		align-items: center;
		gap: 8px;
		max-width: 220px;
	}
</style> 
<script>
	let { confirmGrid, step, run, pause, reset } = $props();
</script>

<div class="simulation-controls">
	<button onclick={confirmGrid}>Confirm Grid</button>
	<button onclick={step}>Step</button>
	<button onclick={run}>Run</button>
	<button onclick={pause}>Pause</button>
	<button onclick={reset}>Reset</button>
</div>

<style>
	.simulation-controls {
		margin-top: 12px;
		display: flex;
		gap: 8px;
	}
</style> 
<script>
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
	import { faPlay, faPause, faStepForward, faCheck, faRedo, faForwardFast } from '@fortawesome/free-solid-svg-icons';
	let { confirmGrid, step, run, pause, reset, runFullAnalysis } = $props();
</script>

<div class="simulation-controls">
	<button class="btn btn-success" onclick={run}><FontAwesomeIcon icon={faPlay} /> </button>
	<button class="btn btn-warning" onclick={pause}><FontAwesomeIcon icon={faPause} /> </button>
	<button class="btn btn-info" onclick={step}><FontAwesomeIcon icon={faStepForward} /> </button>
	<button class="btn btn-secondary" onclick={runFullAnalysis}><FontAwesomeIcon icon={faForwardFast} /> </button>
	<button class="btn btn-danger" onclick={reset}><FontAwesomeIcon icon={faRedo} /> </button>
</div>

<style>
	.simulation-controls {
		display: flex;
		gap: 8px;
	}
</style> 
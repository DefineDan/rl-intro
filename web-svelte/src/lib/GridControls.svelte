<script>
    import {stateLabels} from './constants.js'
	let { selectedStateKind, setSelectedState } = $props();
</script>

<div class="controls">
	{#each Object.entries(stateLabels) as [state, label]}
		<button
			class:active={selectedStateKind === parseInt(state)}
			onclick={() => setSelectedState(parseInt(state))}
		>
			{label}
		</button>
	{/each}
</div>

<style>
	.active {
		background-color: #007bff;
		color: white;
	}
</style> 
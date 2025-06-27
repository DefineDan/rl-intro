<script>
    import {stateLabels, stateBootstrapClasses} from './constants.js'
	let { selectedStateKind, setSelectedState } = $props();

	function getOutlineClass(state) {
		return 'btn ' + (stateBootstrapClasses[state] || 'btn-secondary').replace('btn-', 'btn-outline-');
	}
</script>

<div class="cell-controls">
	{#each Object.entries(stateLabels) as [state, label]}
		<button
			class={`${getOutlineClass(state)}${selectedStateKind === parseInt(state) ? ' active' : ''}`}
			onclick={() => setSelectedState(parseInt(state))}
		>
			{label}
		</button>
	{/each}
</div>

<style>
	.cell-controls button {
		margin: 0.1em;
		margin-top: 0.5em;
	}
</style>

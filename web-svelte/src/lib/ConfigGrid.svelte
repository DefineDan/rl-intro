<script>
    import {stateLabels, stateBootstrapClasses} from './constants.js'
	import { FontAwesomeIcon } from '@fortawesome/svelte-fontawesome';
	import { faTableColumns } from '@fortawesome/free-solid-svg-icons';

	let { selectedStateKind, setSelectedState, addRow, removeRow, addColumn, removeColumn } = $props();

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
<div class="resize-controls-row">
	<button class="btn btn-outline-secondary" onclick={addRow}>+ <FontAwesomeIcon icon={faTableColumns} style="transform: rotate(-90deg);"/></button>
	<button class="btn btn-outline-secondary" onclick={removeRow}>- <FontAwesomeIcon icon={faTableColumns} style="transform: rotate(-90deg);"/></button>
	<button class="btn btn-outline-secondary" onclick={addColumn}>+ <FontAwesomeIcon icon={faTableColumns}/> </button>
	<button class="btn btn-outline-secondary" onclick={removeColumn}>- <FontAwesomeIcon icon={faTableColumns}/></button>
</div>

<style>
	.cell-controls button {
		margin: 0.1em;
		margin-top: 0.5em;
	}
	.resize-controls-row {
		display: flex;
		flex-direction: row;
		align-items: center;
		gap: 0.3rem;
		margin-top: 0.5em;
	}
</style>

<script>
  import { StateKind, stateStyles } from './gridworld.js';
  export let gridState;

  const stateOptions = [
    { kind: StateKind.EMPTY, label: 'Empty' },
    { kind: StateKind.START, label: 'Start' },
    { kind: StateKind.TERMINAL, label: 'Terminal' },
    { kind: StateKind.CLIFF, label: 'Cliff' },
    { kind: StateKind.WALL, label: 'Wall' },
  ];

  $: $gridState = $gridState;

  function selectState(kind) {
    gridState.update(state => ({ ...state, selectedState: kind }));
  }
</script>

<div class="controls-placeholder">
  <div class="cell-type-select">
    {#each stateOptions as opt}
      <button
        type="button"
        class="cell-type-btn {opt.kind === $gridState.selectedState ? 'selected' : ''}"
        style="background: {stateStyles[opt.kind].background}; border: 2px solid {stateStyles[opt.kind].border};"
        on:click={() => selectState(opt.kind)}
      >
        {opt.label}
      </button>
    {/each}
  </div>
</div>

<style>
.controls-placeholder {
  margin: 1rem 0;
  padding: 1rem;
  background: #e0e0e0;
  border-radius: 6px;
  text-align: center;
  color: #666;
}
.cell-type-select {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  margin-bottom: 0.5rem;
}
.cell-type-btn {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  outline: none;
  opacity: 0.85;
  border-width: 2px;
  border-style: solid;
  transition: box-shadow 0.2s, opacity 0.2s;
}
.cell-type-btn.selected {
  box-shadow: 0 0 0 2px #1976d2;
  opacity: 1;
  font-weight: bold;
}
</style> 
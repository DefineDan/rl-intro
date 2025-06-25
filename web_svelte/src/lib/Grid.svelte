<script>
import { StateKind, GridMode, gridWidth } from './gridworld.js';
import GridCell from './GridCell.svelte';

export let gridState;

function handleCellClick(row, col) {
  if ($gridState.mode !== GridMode.CONFIG) return;
  gridState.update(state => {
    const newGrid = state.grid.map(r => [...r]);
    newGrid[row][col] = state.selectedState;
    return { ...state, grid: newGrid };
  });
}
</script>

<div class="grid-container">
  <table class="grid-table">
    <tbody>
      {#each $gridState.grid as row, rowIdx}
        <tr>
          {#each row as kind, colIdx}
            <GridCell
              row={rowIdx}
              col={colIdx}
              kind={kind}
              mode={$gridState.mode}
              agentPos={$gridState.agentPos}
              agentValues={$gridState.agentValues}
              grid={$gridState.grid}
              onCellClick={handleCellClick}
            />
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>
</div>

<style>
.grid-container {
  display: flex;
  justify-content: center;
  margin: 1rem 0;
}
.grid-table {
  border-collapse: collapse;
}
</style> 
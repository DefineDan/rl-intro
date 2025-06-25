<script>
  import { StateKind, stateStyles, GridMode, gridWidth } from './gridworld.js';
  export let row;
  export let col;
  export let kind;
  export let mode;
  export let agentPos;
  export let agentValues;
  export let grid;
  export let onCellClick = () => {};

  // Compute cell style
  function cellStyle() {
    if (mode === GridMode.VALUES && agentValues) {
      const idx = row * gridWidth + col;
      const value = agentValues[idx];
      const min = Math.min(...agentValues);
      const max = Math.max(...agentValues);
      const norm = (value - min) / (max - min || 1);
      // Use a simple blue scale for now; can add d3 later
      const color = `rgba(33, 150, 243, ${0.2 + 0.8 * norm})`;
      return {
        background: color,
        border: `2px solid ${color}`,
        color: '#fff',
      };
    } else {
      const style = stateStyles[kind] || stateStyles[StateKind.EMPTY];
      return {
        background: style.background,
        border: `2px solid ${style.border}`,
      };
    }
  }

  // Compute cell content
  function cellContent() {
    if (
      agentPos &&
      row === agentPos.row &&
      col === agentPos.col
    ) {
      return '🤖';
    }
    if (mode === GridMode.VALUES && agentValues) {
      const idx = row * gridWidth + col;
      return agentValues[idx]?.toFixed(1) ?? '';
    }
    const cellKind = grid[row][col];
    switch (cellKind) {
      case StateKind.START:
        return 'S';
      case StateKind.TERMINAL:
        return 'T';
      case StateKind.CLIFF:
        return 'C';
      case StateKind.WALL:
        return 'W';
      default:
        return '';
    }
  }
</script>

<td
  class="grid-cell"
  style={Object.entries(cellStyle()).map(([k,v]) => `${k}:${v}`).join(';')}
  on:click={() => onCellClick(row, col)}
>
  {cellContent()}
</td>

<style>
.grid-cell {
  width: 36px;
  height: 36px;
  text-align: center;
  vertical-align: middle;
  font-size: 1.2rem;
  cursor: pointer;
  transition: background 0.2s;
  user-select: none;
}
</style> 
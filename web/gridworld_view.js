

const StateKind = {
  EMPTY: 0,
  START: 1,
  TERMINAL: 2,
  CLIFF: 3,
  WALL: 4,
};

// Color/style mapping for each state
const stateStyles = {
  [StateKind.EMPTY]: { background: '#f0f0f0', border: '#ccc' },
  [StateKind.START]: { background: '#4caf50', border: '#388e3c' },
  [StateKind.TERMINAL]: { background: '#2196f3', border: '#1976d2' },
  [StateKind.CLIFF]: { background: '#e53935', border: '#b71c1c' },
  [StateKind.WALL]: { background: '#757575', border: '#424242' },
};

// Render the grid into a container element
function renderGridworld(grid, container, agentPos = null) {
  container.innerHTML = '';
  container.style.display = 'grid';
  container.style.gridTemplateRows = `repeat(${grid.length}, 40px)`;
  container.style.gridTemplateColumns = `repeat(${grid[0].length}, 40px)`;
  container.style.gap = '2px';

  for (let row = 0; row < grid.length; row++) {
    for (let col = 0; col < grid[0].length; col++) {
      const cell = document.createElement('div');
      const kind = grid[row][col];
      const style = stateStyles[kind] || stateStyles[StateKind.EMPTY];
      cell.style.background = style.background;
      cell.style.border = `2px solid ${style.border}`;
      cell.style.width = '40px';
      cell.style.height = '40px';
      cell.style.display = 'flex';
      cell.style.alignItems = 'center';
      cell.style.justifyContent = 'center';
      cell.style.fontWeight = 'bold';
      cell.style.fontSize = '18px';
      cell.style.transition = 'box-shadow 0.2s';
      cell.onmouseenter = () => cell.style.boxShadow = '0 0 8px #888';
      cell.onmouseleave = () => cell.style.boxShadow = '';
      // Optionally, show a symbol for special states
      if (agentPos && row === agentPos.row && col === agentPos.col) {
        cell.textContent = '🤖';
        cell.style.border = '3px solid gold';
      } else if (kind === StateKind.START) cell.textContent = 'S';
      else if (kind === StateKind.TERMINAL) cell.textContent = 'T';
      else if (kind === StateKind.CLIFF) cell.textContent = 'C';
      else if (kind === StateKind.WALL) cell.textContent = 'W';
      container.appendChild(cell);
    }
  }
}

// For standalone test: render into a div with id 'gridworld'
// const dummyGrid = [
//   [1,0,0,0,0,0,0,0,0,2],
//   [0,4,0,3,0,0,0,4,0,0],
//   [0,0,0,0,0,3,0,0,0,0],
//   [0,0,4,0,0,0,0,0,3,0],
// ];

// document.addEventListener('DOMContentLoaded', () => {
//   const container = document.getElementById('gridworld');
//   if (container) {
//     renderGridworld(dummyGrid, container, { row: 0, col: 0 });
//   }
// });

export { renderGridworld, StateKind };

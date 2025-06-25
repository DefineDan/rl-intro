import Alpine from 'https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/module.esm.js';
import { gridWorld } from './grid-world.js';
import { agentConfig } from './agent-config.js';
import { getPyodide } from './pyodide.js';

window.Alpine = Alpine;
window.gridWorld = gridWorld;
window.agentConfig = agentConfig;

document.addEventListener("DOMContentLoaded", () => {
  const output = document.getElementById("output");
  output.textContent = "Initializing Python environment...";

  getPyodide()
    .then(() => {
      output.textContent =
        "Ready! Configure the grid and click Confirm Grid to start.";
    })
    .catch((error) => {
      output.textContent = `Error initializing Python: ${error.message}`;
      console.error(error);
    });

  Alpine.start();
});
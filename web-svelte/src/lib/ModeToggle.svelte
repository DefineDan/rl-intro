<script>
  import { GridMode } from "./constants.js";
  let { mode, agentValues, setMode } = $props();
</script>

<div class="mode-toggle" style="margin-bottom: 12px; display: flex; gap: 8px;">
  <button
    class:active={mode === GridMode.CONFIG}
    onclick={() => setMode(GridMode.CONFIG)}
  >
    Grid Config
  </button>
  <button
    class:active={mode === GridMode.VALUES}
    onclick={() => setMode(GridMode.VALUES)}
    disabled={!agentValues}
  >
    Agent Values
  </button>
</div>

<style>
  .active {
    background-color: #007bff;
    color: white;
  }
</style>

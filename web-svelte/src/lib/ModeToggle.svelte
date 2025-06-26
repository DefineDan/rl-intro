<script>
  import { GridMode } from "./constants.js";
  let { mode, agentValues, setMode } = $props();
</script>

<ul class="nav nav-tabs" role="tablist">
  <li class="nav-item" role="presentation">
    <button
      class="nav-link {mode === GridMode.CONFIG ? 'active' : ''}"
      aria-selected={mode === GridMode.CONFIG}
      role="tab"
      onclick={() => setMode(GridMode.CONFIG)}
      tabindex={mode === GridMode.CONFIG ? 0 : -1}
    >
      Grid Config
  </button>
  </li>
  <li class="nav-item" role="presentation">
    <button
      class="nav-link {mode === GridMode.VALUES ? 'active' : ''} {agentValues ? '' : 'disabled'}"
      aria-selected={mode === GridMode.VALUES}
      role="tab"
      onclick={() => agentValues && setMode(GridMode.VALUES)}
      tabindex={agentValues ? 0 : -1}
      aria-disabled={!agentValues}
    >
      Agent Values
    </button>
  </li>
</ul>

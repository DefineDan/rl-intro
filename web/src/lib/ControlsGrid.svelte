<script>
  import { GridMode } from "./constants.js";
  let { mode, agentValues, agentVisits, setMode } = $props();

  const tabs = [
    {
      label: "Configure",
      mode: GridMode.CONFIG,
      isDisabled: () => false,
      onClick: () => setMode(GridMode.CONFIG),
      tabIndex: () => (mode === GridMode.CONFIG ? 0 : -1),
    },
    {
      label: "View",
      mode: GridMode.VIEW,
      isDisabled: () => false,
      onClick: () => setMode(GridMode.VIEW),
      tabIndex: () => (mode === GridMode.VIEW ? 0 : -1),
    },
    {
      label: "Agent Values",
      mode: GridMode.VALUES,
      isDisabled: () => !agentValues,
      onClick: () => agentValues && setMode(GridMode.VALUES),
      tabIndex: () => (agentValues ? (mode === GridMode.VALUES ? 0 : -1) : -1),
    },
    {
      label: "Agent Visits",
      mode: GridMode.VISITS,
      isDisabled: () => !agentVisits,
      onClick: () => agentVisits && setMode(GridMode.VISITS),
      tabIndex: () => (agentVisits ? (mode === GridMode.VISITS ? 0 : -1) : -1),
    },
  ];
</script>

<ul class="nav nav-tabs" role="tablist">
  {#each tabs as tab}
    <li class="nav-item" role="presentation">
      <button
        class="nav-link {mode === tab.mode ? 'active' : ''} {tab.isDisabled()
          ? 'disabled'
          : ''}"
        aria-selected={mode === tab.mode}
        role="tab"
        onclick={tab.onClick}
        tabindex={tab.tabIndex()}
        aria-disabled={tab.isDisabled()}
      >
        {tab.label}
      </button>
    </li>
  {/each}
</ul>

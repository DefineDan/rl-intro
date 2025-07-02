<script>
    let { config } = $props();
</script>

<div class="card border-primary mb-3 dense-card" style="max-width: 18rem;">
  <div class="card-header" style="padding: 0.4rem 0.8rem; font-size: 1rem;">Experiment Configuration</div>
  <div class="card-body" style="padding: 0.7rem 0.8rem;">
    <div class="experiment-config">
        <label>
            <span>Episodes:</span>
            <input class="form-range small-input" type="range" min="10" max="2000" step="10" bind:value={config.nEpisodes} />
            <span style="min-width:2.5em; text-align:right;">{config.nEpisodes}</span>
        </label>
        <label>
            <span>Max Steps/Episode:</span>
            <input class="form-range small-input" type="range" min="1" max="1000" step="10" bind:value={config.maxSteps} />
            <span style="min-width:2.5em; text-align:right;">{config.maxSteps}</span>
        </label>
    </div>
  </div>
</div>

<style>
    .experiment-config {
        display: flex;
        flex-direction: column;
        gap: 3px;
    }
    label {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.5em;
    }
    .small-input {
        flex: 1;
        margin: 0 0.5em;
    }
</style>

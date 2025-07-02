<script>
  import { AgentType } from "./constants.js";
  let { config } = $props();
</script>

<div class="card border-primary mb-3 dense-card" style="max-width: 18rem;">
  <div class="card-header" style="padding: 0.4rem 0.8rem; font-size: 1rem;">
    Agent Configuration
  </div>
  <div class="card-body" style="padding: 0.7rem 0.8rem;">
    <div class="agent-config">
      <label>
        <span>Agent Type:</span>
        <select
          class="form-select small-input agent-type-select"
          bind:value={config.agentType}
        >
          <option value={AgentType.EXPECTED_SARSA}>Expected Sarsa</option>
          <option value={AgentType.Q_LEARNING}>Q-Learning</option>
          <option value={AgentType.SARSA}>Sarsa</option>
        </select>
      </label>
      <label>
        <span>Learning Rate:</span>
        <input
          class="input-group-text small-input"
          type="number"
          step="0.01"
          min="0"
          max="1"
          bind:value={config.learningRate}
        />
      </label>
      <label>
        <span>Discount:</span>
        <input
          class="input-group-text small-input"
          type="number"
          step="0.01"
          min="0"
          max="1"
          bind:value={config.discount}
        />
      </label>
      <label>
        <span>Epsilon:</span>
        <input
          class="input-group-text small-input"
          type="number"
          step="0.01"
          min="0"
          max="1"
          bind:value={config.epsilon}
        />
      </label>
    </div>
  </div>
</div>

<style>
  .agent-config {
    display: flex;
    flex-direction: column;
    gap: 3px;
  }

  label {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .small-input {
    font-size: 0.92rem;
    padding: 2px 6px;
    height: 1.7rem;
    min-width: 3.5rem;
    border-radius: 3px;
  }

  .agent-type-select {
    min-width: 6.5rem;
    width: 8.5rem;
    max-width: 10rem;
  }
</style>

<script>
    import { AgentType } from './constants.js';

    let { config } = $props();
</script>

<div class="agent-config">
    <label>
        Agent Type:
        <select bind:value={config.agentType}>
            <option value={AgentType.EXPECTED_SARSA}>Expected Sarsa</option>
            <option value={AgentType.Q_LEARNING}>Q-Learning</option>
            <option value={AgentType.SARSA}>Sarsa</option>
        </select>
    </label>
    <label>
        Learning Rate:
        <input type="number" step="0.01" min="0" max="1" bind:value={config.learningRate} />
    </label>
    <label>
        Discount:
        <input type="number" step="0.01" min="0" max="1" bind:value={config.discount} />
    </label>
    <label>
        Epsilon:
        <input type="number" step="0.01" min="0" max="1" bind:value={config.epsilon} />
    </label>
</div>

<style>
    .agent-config {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 12px;
        padding: 12px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    label {
        display: flex;
        justify-content: space-between;
    }
</style> 
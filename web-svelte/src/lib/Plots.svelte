<script>
    import { onMount } from "svelte";
    import { plotCumulativeReward, plotEpisodicRewards } from "./plot.js";

    let { cumulativeReward, episodicRewards } = $props();
    $effect(() => {
        plotCumulativeReward(cumulativeReward);
        plotEpisodicRewards(episodicRewards);
    });
</script>

<div class="plots-row">
    <div id="reward-plot" class="plot-container"></div>
    <div id="episodic-reward-plot" class="plot-container"></div>
</div>

<style>
    .plots-row {
        display: flex;
        flex-direction: row;
    }
    .plot-container {
        width: 50%;
        height: 17em;
    }
</style>

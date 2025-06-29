<script>
    import { onMount } from "svelte";
    import { plotCumulativeReward, plotEpisodicRewards } from "./plot.js";

    let { cumulativeReward, episodicRewards } = $props();
    const uniqueId = Math.random().toString(36).substr(2, 9);
    const rewardPlotId = `reward-plot-${uniqueId}`;
    const episodicRewardPlotId = `episodic-reward-plot-${uniqueId}`;
    
    $effect(() => {
        plotCumulativeReward(cumulativeReward, rewardPlotId);
        plotEpisodicRewards(episodicRewards, episodicRewardPlotId);
    });
</script>

<div class="plots-row">
    <div id={rewardPlotId} class="plot-container"></div>
    <div id={episodicRewardPlotId} class="plot-container"></div>
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

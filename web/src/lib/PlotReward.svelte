<script>
    import { onMount } from "svelte";
    import { plotCumulativeReward, plotEpisodicRewards } from "./plot.js";

    let { cumulativeReward, episodicRewards, simId } = $props();
    const rewardPlotId = `reward-plot-${simId}`;
    const episodicRewardPlotId = `episodic-reward-plot-${simId}`;
    
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

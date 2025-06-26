import Plotly from 'plotly.js-dist-min'


function plotCumulativeReward(cumulativeReward, containerId = "reward-plot") {
  const globalStepIdx = cumulativeReward.columns.indexOf("global_step");
  if (globalStepIdx === -1) {
    console.error("global_step column not found in cumulativeReward");
    return;
  }
  const globalSteps = cumulativeReward.data.map(row => row[globalStepIdx]);

  const traces = [];
  cumulativeReward.columns.forEach((col, i) => {
    if (col === "global_step") return;
    const yValues = cumulativeReward.data.map(row => row[i]);
    traces.push({
      x: globalSteps,
      y: yValues,
      mode: 'lines',
      name: col,
      line: { width: 2 },
    });
  });

  const layout = {
    title: 'Cumulative Reward',
    xaxis: { title: 'Global Step' },
    yaxis: { title: 'Reward' },
    margin: { t: 40, r: 30, b: 40, l: 50 },
    legend: { x: 1, y: 1 },
    width: 600,
    height: 300,
  };

  Plotly.newPlot(containerId, traces, layout, {responsive: true});
}

function plotEpisodicRewards(episodicRewards, containerId = "episodic-reward-plot") {
  const episodeIdx = episodicRewards.columns.indexOf("episode");
  const rewardIdx = episodicRewards.columns.indexOf("reward");
  if (episodeIdx === -1 || rewardIdx === -1) {
    console.error("episode or reward column not found in episodicRewards");
    return;
  }
  const episodes = episodicRewards.data.map(row => row[episodeIdx]);
  const rewards = episodicRewards.data.map(row => row[rewardIdx]);

  const trace = {
    x: episodes,
    y: rewards,
    mode: 'lines',
    name: 'Reward',
    line: { width: 2 },
  };

  const layout = {
    title: 'Episodic Reward',
    xaxis: { title: 'Episode' },
    yaxis: { title: 'Reward' },
    margin: { t: 40, r: 30, b: 40, l: 50 },
    legend: { x: 1, y: 1 },
    width: 600,
    height: 300,
  };

  Plotly.newPlot(containerId, [trace], layout, {responsive: true});
}

export { plotCumulativeReward, plotEpisodicRewards };
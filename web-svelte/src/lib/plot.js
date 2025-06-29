import Plotly from 'plotly.js-dist-min'


function plotCumulativeReward(cumulativeReward, containerId) {
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
      line: { width: 2, color: '#6f42c1' },
      hovertemplate: 'Global Step: %{x}<br>Accumulated Reward: %{y}<extra></extra>',
    });
  });

  const layout = {
    title: 'Cumulative Reward',
    xaxis: { title: 'Global Step', gridcolor: 'rgba(224,224,224,0.1)' },
    yaxis: { title: 'Reward', gridcolor: 'rgba(224,224,224,0.1)' },
    margin: { t: 40, r: 30, b: 40, l: 50 },
    legend: { x: 1, y: 1 },
    plot_bgcolor: 'rgba(0,0,0,0)',
    paper_bgcolor: 'rgba(0,0,0,0)',
  };

  Plotly.newPlot(containerId, traces, layout, {responsive: true});
}

function plotEpisodicRewards(episodicRewards, containerId) {
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
    line: { width: 2, color: '#6f42c1' },
    hovertemplate: 'Episode: %{x}<br>Reward: %{y}<extra></extra>',
  };

  const layout = {
    title: 'Episodic Reward',
    xaxis: { title: 'Episode', gridcolor: 'rgba(224,224,224,0.1)' },
    yaxis: { title: 'Reward', gridcolor: 'rgba(224,224,224,0.1)' },
    margin: { t: 40, r: 30, b: 40, l: 50 },
    legend: { x: 1, y: 1 },
    plot_bgcolor: 'rgba(0,0,0,0)',
    paper_bgcolor: 'rgba(0,0,0,0)',
  };

  Plotly.newPlot(containerId, [trace], layout, {responsive: true});
}

export { plotCumulativeReward, plotEpisodicRewards };
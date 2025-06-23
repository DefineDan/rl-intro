function plotCumulativeReward(cumulativeReward, containerId = "reward-plot") {
  // Remove any previous SVG
  d3.select(`#${containerId}`).selectAll("*").remove();

  const margin = {top: 20, right: 30, bottom: 30, left: 50};
  const width = 600 - margin.left - margin.right;
  const height = 300 - margin.top - margin.bottom;

  const svg = d3.select(`#${containerId}`)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Find the index of the global_step column
  const globalStepIdx = cumulativeReward.columns.indexOf("global_step");
  if (globalStepIdx === -1) {
    console.error("global_step column not found in cumulativeReward");
    return;
  }
  const globalSteps = cumulativeReward.data.map(row => row[globalStepIdx]);

  // Plot each other column as a line
  cumulativeReward.columns.forEach((col, i) => {
    if (col === "global_step") return; // skip x-axis

    const yValues = cumulativeReward.data.map(row => row[i]);
    const y = d3.scaleLinear()
      .domain([d3.min(yValues), d3.max(yValues)])
      .range([height, 0]);

    // X axis
    const x = d3.scaleLinear()
      .domain(d3.extent(globalSteps))
      .range([0, width]);

    if (i === 1) { // Only add axes once
      svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));
      svg.append("g")
        .call(d3.axisLeft(y));
    }

    const line = d3.line()
      .x((d, idx) => x(globalSteps[idx]))
      .y((d) => y(d));

    svg.append("path")
      .datum(yValues)
      .attr("fill", "none")
      .attr("stroke", d3.schemeCategory10[(i-1) % 10])
      .attr("stroke-width", 2)
      .attr("d", line);

    // Add legend
    svg.append("text")
      .attr("x", width - 60)
      .attr("y", 20 + (i-1) * 20)
      .attr("fill", d3.schemeCategory10[(i-1) % 10])
      .text(col);
  });
}

function plotEpisodicRewards(episodicRewards, containerId = "episodic-reward-plot") {
  d3.select(`#${containerId}`).selectAll("*").remove();

  const margin = {top: 20, right: 30, bottom: 30, left: 50};
  const width = 600 - margin.left - margin.right;
  const height = 300 - margin.top - margin.bottom;

  const svg = d3.select(`#${containerId}`)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Find the index of the episode and reward columns
  const episodeIdx = episodicRewards.columns.indexOf("episode");
  const rewardIdx = episodicRewards.columns.indexOf("reward");
  if (episodeIdx === -1 || rewardIdx === -1) {
    console.error("episode or reward column not found in episodicRewards");
    return;
  }
  const episodes = episodicRewards.data.map(row => row[episodeIdx]);
  const rewards = episodicRewards.data.map(row => row[rewardIdx]);

  const x = d3.scaleLinear()
    .domain(d3.extent(episodes))
    .range([0, width]);
  const y = d3.scaleLinear()
    .domain([d3.min(rewards), d3.max(rewards)])
    .range([height, 0]);

  // X axis
  svg.append("g")
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisBottom(x));
  // Y axis
  svg.append("g")
    .call(d3.axisLeft(y));

  // Draw the line
  const line = d3.line()
    .x((d, idx) => x(episodes[idx]))
    .y((d) => y(d));

  svg.append("path")
    .datum(rewards)
    .attr("fill", "none")
    .attr("stroke", d3.schemeCategory10[0])
    .attr("stroke-width", 2)
    .attr("d", line);

  // Add legend
  svg.append("text")
    .attr("x", width - 60)
    .attr("y", 20)
    .attr("fill", d3.schemeCategory10[0])
    .text("Reward");
}

// Make it available globally
window.plotCumulativeReward = plotCumulativeReward;
window.plotEpisodicRewards = plotEpisodicRewards; 
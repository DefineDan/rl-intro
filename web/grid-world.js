import { GridMode, StateKind, stateStyles, initialGrid, stateLabels } from './constants.js';
import { getPyodide } from './pyodide.js';
import { plotCumulativeReward, plotEpisodicRewards } from './plot.js';
import * as pyInterface from './py-interface.js';

export function gridWorld() {
  return {
    GridMode, // Make GridMode available to Alpine.js
    stateLabels,
    grid: JSON.parse(JSON.stringify(initialGrid)),
    selectedState: StateKind.EMPTY,
    agentPos: null,
    gridWidth: 10,
    mode: GridMode.CONFIG,
    agentValues: null,
    isRunning: false,
    stepInterval: null,
    stepDelay: 200, // Default delay in ms

    getCellStyle(kind, row, col) {
      if (this.mode === GridMode.VALUES && this.agentValues) {
        const idx = row * this.gridWidth + col;
        const value = this.agentValues[idx];
        const min = Math.min(...this.agentValues);
        const max = Math.max(...this.agentValues);
        const norm = (value - min) / (max - min || 1);
        const color = d3.interpolateViridis(norm);
        return {
          background: color,
          border: `2px solid ${color}`,
          color: "#fff",
        };
      } else {
        const style = stateStyles[kind] || stateStyles[StateKind.EMPTY];
        return {
          background: style.background,
          border: `2px solid ${style.border}`,
        };
      }
    },

    getCellContent(row, col) {
      if (
        this.agentPos &&
        row === this.agentPos.row &&
        col === this.agentPos.col
      ) {
        return "🤖";
      }
      if (this.mode === GridMode.VALUES && this.agentValues) {
        const idx = row * this.gridWidth + col;
        return this.agentValues[idx].toFixed(1);
      }
      const kind = this.grid[row][col];
      switch (kind) {
        case StateKind.START:
          return "S";
        case StateKind.TERMINAL:
          return "T";
        case StateKind.CLIFF:
          return "C";
        case StateKind.WALL:
          return "W";
        default:
          return "";
      }
    },

    updateCell(row, col) {
      if (this.mode !== GridMode.CONFIG) return;
      this.grid[row][col] = this.selectedState;
    },


    async confirmGrid() {
      const output = document.getElementById("output");
      output.textContent = "Initializing simulation...";

      try {
        let agentConfig = window.agentConfigInstance.getConfig();
        await pyInterface.initializeSimulation(this.grid, agentConfig);
        this.agentPos = await pyInterface.getCurrentPosition();

        output.textContent = "Simulation initialized. Ready to step or run.";
      } catch (error) {
        output.textContent = `Error: ${error.message}`;
        console.error(error);
      }
    },

    async step() {
      const output = document.getElementById("output");
      try {
        const stepResult = await pyInterface.stepExperiment();

        this.agentPos = stepResult.position;
        this.agentValues = stepResult.values;
        output.textContent = `Episode: ${stepResult.step_log.episode}, Step: ${
          stepResult.step_log.step
        }, Reward: ${stepResult.step_log.reward.toFixed(2)}`;

        if (stepResult.step_log.terminal) {
          output.textContent += " (Episode finished)";
        }
      } catch (error) {
        output.textContent = `Error: ${error.message}`;
        console.error(error);
        this.pause();
      }
    },

    run() {
      this.pause();
      this.isRunning = true;
      this.stepInterval = setInterval(() => {
        this.step();
      }, this.stepDelay);
    },

    pause() {
      this.isRunning = false;
      if (this.stepInterval) {
        clearInterval(this.stepInterval);
        this.stepInterval = null;
      }
    },

    reset() {
      this.pause();
      this.mode = GridMode.CONFIG;
      this.agentPos = null;
      this.agentValues = null;
      const output = document.getElementById("output");
      output.textContent =
        "Ready! Configure the grid and click Confirm Grid to start.";
    },

    async runFullAnalysis() {
      const output = document.getElementById("output");
      output.textContent = "Running full analysis...";

      try {
        this.pause();
        let agentConfig = window.agentConfigInstance.getConfig();
        await pyInterface.initializeSimulation(this.grid, agentConfig);
        await pyInterface.runFullExperiment();
        const results = await pyInterface.analyzeExperimentLogs();

        const cumulativeReward = JSON.parse(results.cumulative_reward);
        const episodicRewards = JSON.parse(results.episodic_rewards);

        plotCumulativeReward(cumulativeReward, "reward-plot");
        plotEpisodicRewards(episodicRewards, "episodic-reward-plot");

        this.agentPos = await pyInterface.getCurrentPosition();
        this.agentValues = results.values;

        output.textContent = "Analysis complete!";
      } catch (error) {
        output.textContent = `Error: ${error.message}`;
        console.error(error);
      }
    },
  };
} 
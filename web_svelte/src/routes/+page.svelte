<script>
  import Grid from '$lib/Grid.svelte';
  import Controls from '$lib/Controls.svelte';
  import Stats from '$lib/Stats.svelte';
  import { createGridState, initialGrid } from '$lib/gridworld.js';

  // Create one grid instance (can create more for multiple grids)
  const gridState = createGridState(initialGrid);
</script>

<main>
  <h1>RL Gridworld Demo (Svelte)</h1>
  <Controls {gridState} />
  <Grid {gridState} />
  <Stats />
</main>

<style>
main {
  max-width: 700px;
  margin: 2rem auto;
  padding: 1rem;
  font-family: system-ui, sans-serif;
}
h1 {
  text-align: center;
  margin-bottom: 2rem;
}
</style>

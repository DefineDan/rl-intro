<script>
  import Latex from "$lib/LaTeX.svelte";
</script>

<h1>Model-based Reinforcement Learning</h1>

<div class="card border-secondary mb-3">
  <div class="card-header">Coming soon...</div>
  <div class="card-body">
    <p class="card-text">
      Here we'll talk about methods that learn a model of the environment and
      use it to plan actions. In addition to real experience, the agent can use
      the model to simulate future actions and their outcomes, and thus learn
      from simulated experience. We'll take a look at methods like Dyna-Q and
      more. For now take a look at
      <a href="/tabular-methods" class="alert-link">Tabular Methods</a>
      to get started with the basics of reinforcement learning.
    </p>
  </div>
</div>

<style>
  .card {
    max-width: 60%;
    margin: auto;
    margin-top: 5em;
  }
  p {
    margin: 0;
  }
  h1 {
    text-align: center;
  }
</style>

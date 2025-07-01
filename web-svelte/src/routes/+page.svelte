<script>
  import Simulation from "$lib/Simulation.svelte";
  import Latex from "$lib/LaTeX.svelte";
</script>

<h1>An Interactive Introduction to Reinforcement Learning</h1>

<p>
  This is an interactive playground for exploring basic concepts of
  Reinforcement Learning, an approach to machine learning concerned with agents
  that learn from their environment by exploration and experience. While there
  are excellent theoretical explanations, most notably <a
    href="http://incompleteideas.net/book/the-book-2nd.html"
    >Reinforcement Learning: An Introduction by Sutton and Barto</a
  >, this site aims to provide some intuition on basic algorithms, parameters
  and their shortcomings. Just like our agents we learn best by trial and error
  and exploration.
</p>
<div class="alert alert-dismissible alert-primary">
  <button
    type="button"
    class="btn-close"
    data-bs-dismiss="alert"
    aria-label="Close"
  ></button>
  Start here at
  <a href="/tabular-methods" class="alert-link">Tabular Methods</a> or read below
  if you're interested in implementation details.
</div>

<h3>Technical Details</h3>
<p>
  As you can see below you can configure and run experiments right here in your
  browser. Since simulating agent environment interactions for reinforcement
  learning can be compute intensive, a design goal of this project was to run
  everything on the client side without any backend. On the other hand, the
  machine learning (including the reinforcement learning) community operates in
  Python and even though it is absolutely possible to implement the simple
  concepts here in JavaScript (or any flavour of it) the goal was to keep the
  core logic in Python and only use the web as the interface. The solution comes
  in the form of web assembly (<a href="https://webassembly.org/">WASM</a>).
  With <a href="https://pyodide.org/en/stable/#">Pyodide</a> you can execute
  Python code in the browser's JavaScript runtime. This way the RL core is
  completely reusable and we can run experiments as classic Python scripts or
  from e.g. Jupyter notebooks as well! The lean and fully typed
  <a href="https://github.com/DefineDan/rl-intro/tree/main/rl_intro">
    Python package
  </a>
  is built into a wheel, which we can import and use with Pyodide. The front end,
  as always, is a matter of personal preference. While this started out as plain
  JS, the right framework can provide the right balance of convenience and capability.
  This site is built with <a href="https://svelte.dev/">Svelte</a>, which is,
  compared to React, surprisingly pleasant to work with, while being fast as
  it's compiled to plain JS. This also makes it super easy to host, as here on
  GitHub pages right along the
  <a href="https://github.com/DefineDan/rl-intro">source code</a>.
</p>

<h3>Playground</h3>
Have a go at it! You can build your environment and configure the agent. For a bit
of background head over to
<a href="/tabular-methods"> Tabular Methods</a>.

<Simulation id="home-simulation" />

<script>
	import Simulation from "$lib/Simulation.svelte";
	import Latex from "$lib/LaTeX.svelte";
</script>

<h1>An Interactive Introduction to Reinforcement Learning</h1>

<p>This is an interactive playground for exploring basic concepts of Reinforcement Learning, 
	an approach of machine learning concerned with agents that learn from their environment by exploration and experience.
	While there are excellent theoretical explanations, most notably the popular book <a href=http://incompleteideas.net/book/the-book-2nd.html>Reinforcement Learning: An Introduction by Sutton and Barto</a>,
	this site aims to provide some intuition on basic algorithms, parameters and their shortcomings. 
	Just like our agents we learn best by trial and error and exploration.
</p>

<h3>Technical Details</h3>
<p>


As you can see <a href="#home-simulation" on:click={() => document.getElementById('home-simulation')?.scrollIntoView({ behavior: 'smooth' })}>below</a>
you can run experiments right here in your browser. Since simulating agent environment interactions for reinforcement learning
can be compute intense, a design goal of this project was to run everything on the client side without any backend. 
On the other hand, the machine learning(including the reinforcement learning) community operates in Python 
and even though it is absolutely possible to implement the simple concepts here in javascript (or any flavour of it)
the goal was to keep the core logic in python and only use the web as the interface.
The solution comes in the form of web assembly (<a href="https://webassembly.org/">WASM</a>).
With <a href="https://pyodide.org/en/stable/#">Pyodide</a> you can execute python code in the browser's JavaScript runtime.
This way the RL core is completely reusable and we can run experiments as classic python scripts or from e.g. jupyter notebooks as well!
The lean and fully typed <a href="https://github.com/DefineDan/rl-intro/tree/main/rl_intro"> python package </a> 
is built into a wheel, which we can import and use with pyodide.
The front end, as always, is a matter of personal preference. 
While this started out as plain JS, the right framework can provide the right
balance of convenience and capability. This site is built with <a href="https://svelte.dev/">Svelte</a>, 
which is, compared to React, surprisingly pleasant to work with, while being fast as it's compiled to plain JS.
This also makes it super easy to host, as here on github pages.
</p>

<h3>Playground</h3>
Have a go at it! You can build your environment and configure the agent. For a bit of background head over to
<a href="/tabular-methods"> Tabular Methods</a>.

<Simulation id="home-simulation" />

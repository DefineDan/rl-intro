<script>
	import Simulation from "$lib/Simulation.svelte";
	import Latex from "$lib/LaTeX.svelte";

	let math =
		"Q(s,a) \\leftarrow Q(s,a) + \\alpha \\left( r + \\gamma \\sum_{a'} Q(s', a') - Q(s,a) \\right)";
</script>

<h1>Introduction to Reinforcement Learning</h1>
<p>This is a simple reinforcement learning simulation built with Svelte.</p>
<p>
	Q-learning update rule: <Latex {math} />
</p>
<Simulation />

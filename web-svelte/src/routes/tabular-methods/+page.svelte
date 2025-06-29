<script>
	import Simulation from "$lib/Simulation.svelte";
	import Latex from "$lib/LaTeX.svelte";
    import { AgentType } from '../../lib/constants'

	let qLearningMath = "Q(s,a) \\leftarrow Q(s,a) + \\alpha \\left( r + \\gamma \\max_{a'} Q(s', a') - Q(s,a) \\right)";
	let sarsaMath = "Q(s,a) \\leftarrow Q(s,a) + \\alpha \\left( r + \\gamma Q(s', a') - Q(s,a) \\right)";
	let expectedSarsaMath = "Q(s,a) \\leftarrow Q(s,a) + \\alpha \\left( r + \\gamma \\sum_{a'} \\pi(a'|s') Q(s', a') - Q(s,a) \\right)";
</script>

<h1>Tabular Reinforcement Learning Methods</h1>

<p>
	Tabular reinforcement learning methods.
</p>


<h2>Q-Learning</h2>


<p>
	<Latex math={qLearningMath} displayMode/>
</p>
<Simulation agentType={AgentType.Q_LEARNING}/> 

<h2>Sarsa</h2>

<p>
	<Latex math={sarsaMath} displayMode/>
</p>
<Simulation agentType={AgentType.SARSA}/> 


<h2>Expected Sarsa</h2>


<p>
	<Latex math={expectedSarsaMath} displayMode/>
</p>
<Simulation agentType={AgentType.EXPECTED_SARSA}/> 
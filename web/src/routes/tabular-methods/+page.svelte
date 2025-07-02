<script>
  import Simulation from "$lib/Simulation.svelte";
  import Latex from "$lib/LaTeX.svelte";
  import CodeBlock from "$lib/CodeBlock.svelte";
  import { AgentType } from "../../lib/constants";
  import Grid from "$lib/Grid.svelte";
  import { initialGrid } from "$lib/constants.js";
</script>

<h1>Tabular Reinforcement Learning Methods</h1>

<p>
  Tabular reinforcement learning methods only work for small state and action
  spaces so that the agent's value function can be represented in a simple
  <b>tabular data structure</b>. Most interesting RL problems don't fall into
  that category because the state space is either too large (think games like
  chess or go), or state and action space might even be continuous (think robot
  control). While
  <a href="/function-approximation"> Function Approximation</a>
  can be used in those cases, for now we stick to a conveniently <b>discrete</b>
  and <b>small</b> <b>state-action space</b>.
</p>

<h2>Gridworld Environment</h2>
<div class="gridworld-section">
  <p>
    Gridworld is a simple environment to showcase the most basic tabular
    learning mechanisms and is basically a maze. It contains <b>start</b> and
    <b>terminal</b>
    states, which makes this an <b>episodic RL problem </b>. Further we
    introduce
    <b>wall</b>
    and <b>cliff</b> states, the reason this problem is sometimes called cliff walk.
    There are only four possible actions for the agent. The reward function is simple
    and encourages finding the shortest path to the terminal state.
  </p>
  <Grid grid={initialGrid} />
</div>

<CodeBlock
  code="def default_reward_function(state: State, kind: StateKind) -> Reward:
    if kind == StateKind.CLIFF.value:
        return -100.0
    elif kind == StateKind.TERMINAL.value:
        return 1.0
    else:
        return -1.0"
  sourceUrl="https://github.com/DefineDan/rl-intro/blob/main/rl_intro/environment/gridworld.py"
/>

<h2>Temporal Difference Learning Agents</h2>
<p>
  Here we will investigate three tightly related learning RL algorithms. In
  their core they are all temporal difference (<b>TD</b>) learning algorithms,
  meaning they learn on every timestamp throughout the interaction (<b
    >online learning</b
  >). The methods learn the <b>action-value function</b>
  <Latex math="Q(s,a)" /> predicting the expected future reward (return) when being
  in state <Latex math="s" /> and taking action <Latex math="a" />. It is used
  by the policy to decide on the next action to take. The methods presented here
  are <b>model-free</b>, so they don't attempt to model the environment dynamics
  and they are <b>bootstrapping</b> as they update Q-values using learned
  Q-value estimates. The general update rule or learning step where
  <Latex math={"\\delta_{TD}"} /> is the TD error,
  <Latex math="\alpha" /> is the learning rate,
  <Latex math="r" /> is the immediate reward,
  <Latex math="\gamma" /> is the discount factor and
  <Latex math="V(s')" /> is the value of the next state can be defined as:
  <Latex math={"\\delta_{TD} = r + \\gamma V(s') - Q(s,a)"} displayMode />
  <Latex
    math={"Q(s,a) \\leftarrow Q(s,a) + \\alpha \\delta_{TD}"}
    displayMode
  />
</p>

<h3>Policies</h3>
<p>
  Predicting Q-values is one thing. However, the agent still has to decide what
  action to take. Here we use the simple <b>ε-greedy policy </b>
  as it highlights the important <b>exploration exploitation tradeoff</b> in RL
  nicely. Other policies, such as softmax action selection or Upper Confidence
  Bound (UCB) offer alternatives to balance this tradeoff. For the ε-greedy
  policy the agent chooses a random action with probability <Latex
    math="\epsilon"
  />
  (exploration) otherwise it will take the action with the currently highest Q-value,
  the greedy action (exploitation).
  <Latex
    math={"\\pi(a|s) = \\begin{cases}1 - \\epsilon + \\frac{\\epsilon}{|A|} & \\text{if } a = \\argmax_{a'} Q(s,a') \\\\ \\frac{\\epsilon}{|A|} & \\text{otherwise}\\end{cases}"}
    displayMode
  />
</p>

<h2>Sarsa</h2>

<p>
  Sarsa is an <b>on-policy</b> control method and got its name from the elements
  used to compute the update. We call it on-policy because it uses the current
  policy <Latex math={"\\pi(a|s)"} /> to select the next action <Latex
    math={"a'"}
  />. Sarsa can find an optimal policy <Latex math={"\\pi^*"} /> by greedifying towards
  the end of the learning process, but it will always follow the current policy during
  learning. With sampling <Latex math="a' \sim \pi" />, the update rule follows
  as:
</p>
<Latex
  math={"Q(s,a) \\leftarrow Q(s,a) + \\alpha \\left( r + \\gamma Q(s', a') - Q(s,a) \\right)"}
  displayMode
/>

<Simulation agentType={AgentType.SARSA} />

<h3>Q-Learning</h3>
<p>
  Q-Learning is an <b>off-policy</b> control method, meaning it can learn the
  optimal policy (the target policy) <Latex math={"\\pi^*"} /> while following a
  different policy <Latex math={"\\pi^*"} /> (the behaviour policy). Here the target
  policy is a greedy policy, which is given the correct Q-values, an optimal policy.
</p>
<Latex
  math={"Q(s,a) \\leftarrow Q(s,a) + \\alpha \\left( r + \\gamma \\max_{a'} Q(s', a') - Q(s,a) \\right)"}
  displayMode
/>

<p>
  You might observe that Q-learning takes a riskier path towards the terminal
  state, as it is not accounting for the explorative actions of the behavior
  policy. This results in lower rewards during the learning process, but in the
  end it will find the optimal policy.
</p>

<Simulation agentType={AgentType.Q_LEARNING} />

<h3>Expected Sarsa</h3>
<p>
  Expected Sarsa uses the expected value under the policy <Latex math="\pi" /> to
  compute updates and thereby is not affected by the sampling variance like Sarsa.
  While in expectation they learn the same, expected Sarsa is usually more robust
  at the cost of computation. Sarsa can be used for both on-policy and off-policy
  learning, as <Latex math="\pi" /> can be different from the policy we choose to
  select the next action <Latex math="a' \sim \pi_b" />. We can see expected
  Sarsa as a generalization of Q-learning where <Latex
    math="{'\\pi = \\pi_{greedy}'}."
  />
</p>
<Latex
  math={"Q(s,a) \\leftarrow Q(s,a) + \\alpha \\left( r + \\gamma \\sum_{a'} \\pi(a'|s') Q(s', a') - Q(s,a) \\right)"}
  displayMode
/>

<Simulation agentType={AgentType.EXPECTED_SARSA} />

<h2>Implementation</h2>
<p>
  The agent implementations are fairly simple. Take a look here at the code at <a
    href="https://github.com/DefineDan/rl-intro/tree/main/rl_intro/agent"
    >rl-intro on GitHub</a
  >.
</p>
<CodeBlock
  code="def learn(
        self, state: State, reward: Reward, terminal: Terminal, action: Action
    ) -> None:
        if terminal:
            td_error = reward - self.q[self.last_state, self.last_action]
        else:
            td_error = (
                reward
                + self.config.discount * np.max(self.q[state, :])
                - self.q[self.last_state, self.last_action]
            )
        self.q[self.last_state, self.last_action] += (
            self.config.learning_rate * td_error
        )"
  sourceUrl="https://github.com/DefineDan/rl-intro/blob/main/rl_intro/agent/agent_q_learning.py"
/>

<style>
  .gridworld-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    gap: 2rem;
    margin-bottom: 1em;
  }
</style>

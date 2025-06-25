import { AgentType } from './constants.js';

export function agentConfig() {
  return {
    AgentType, // Make AgentType available to the template
    agentType: AgentType.EXPECTED_SARSA,
    learningRate: 0.3,
    discount: 1.0,
    epsilon: 0.1,
    getConfig() {
      return {
        agent_type: this.agentType,
        learning_rate: this.learningRate,
        discount: this.discount,
        epsilon: this.epsilon,
      };
    },
  };
} 
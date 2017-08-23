# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        #we just need to follow the recurise definition of value,and need to take care of terminal state
        for i in range(self.iterations):
          newValues=self.values.copy()
          for state in self.mdp.getStates():
            if self.mdp.isTerminal(state):
              self.values[state]=0
            else:
              maxQ=float("-inf")
              for action in self.mdp.getPossibleActions(state):
                if(maxQ<self.computeQValueFromValues(state,action)):
                  maxQ=self.computeQValueFromValues(state,action)
              newValues[state]=maxQ
          self.values=newValues



    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #We just need to calculte the QValue as the resurise definition of the MDP 
        QValue=0
        for nextState,probablity in self.mdp.getTransitionStatesAndProbs(state,action):
          QValue=QValue+probablity*(self.mdp.getReward(state,action,nextState)+self.discount*self.getValue(nextState))
        return QValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        #if it's terminal state, return None.
        if self.mdp.isTerminal(state):
          return None
        #if not the terminal state,computer all the qvalue when given the (state,action),find the max value and return
        values=util.Counter()
        for action in self.mdp.getPossibleActions(state):
          values[action]=self.computeQValueFromValues(state,action)
        return values.argMax()


    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states=self.mdp.getStates()
        for i in range(self.iterations):
          state=states[i%len(states)]
          if self.mdp.isTerminal(state):
            self.values[state]=0
          else:
            maxQ=float("-inf")
            for action in self.mdp.getPossibleActions(state):
              if(maxQ<self.computeQValueFromValues(state,action)):
                maxQ=self.computeQValueFromValues(state,action)
            self.values[state]=maxQ


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        #Firstly, Compute predecessors of all states
        predecessors = {}
        for state in self.mdp.getStates():
            predecessors[state] = set()
        for state in self.mdp.getStates():
            for action in self.mdp.getPossibleActions(state):
                for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                    if prob >= self.theta:
                        predecessors[nextState].add(state)
        #Initialize an empty priority queue.
        diffs = util.PriorityQueue()
        #For each non-terminal state s, do what the question
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                maxQ = float("-inf")
                for action in self.mdp.getPossibleActions(state):
                    if(maxQ<self.computeQValueFromValues(state,action)):
                      maxQ=self.computeQValueFromValues(state,action)
                diff = abs(self.values[state] - maxQ)
                diffs.push(state, -diff)
        #For iteration in 0, 1, 2, ..., self.iterations - 1, Do the algoritm asked
        for i in range(self.iterations):
            if diffs.isEmpty():
                break
            state = diffs.pop()
            if not self.mdp.isTerminal(state):
                maxQ = float("-inf")
                for action in self.mdp.getPossibleActions(state):
                    if(maxQ<self.computeQValueFromValues(state,action)):
                      maxQ=self.computeQValueFromValues(state,action)
                self.values[state] = maxQ
            for p in predecessors[state]:
                maxQ = float("-inf")
                for action in self.mdp.getPossibleActions(p):
                    if(maxQ<self.computeQValueFromValues(p,action)):
                      maxQ=self.computeQValueFromValues(p,action)
                diff = abs(self.values[p] - maxQ)
                if diff > self.theta:
                  diffs.update(p, -diff)
        


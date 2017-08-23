# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        #print "********************************************************************"
        #print "successorGameState:",successorGameState #cunrrent state about the whole game(a graph reresentation)
        #print "newPos:", newPos                 #cunrrent pacman's position                                                              
        #print "newFood:", newFood               #a graph resresentation the food state(true or false)
        #print "newGhostStates:",newGhostStates  #cunrrent ghostState
        #print "newScaredTimes:",newScaredTimes
        #print "*********************************************************************"
       
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 1)
    """
    
   
    def getAction(self, gameState):
        
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        
        legalMoves=gameState.getLegalActions(0)
        bestScore=float("-inf")
        bestMove=''
        for move in legalMoves:
            tempScore = self.getValue(gameState.generateSuccessor(0, move), 1 , 1)
            if  bestScore < tempScore :
                bestScore = tempScore
                bestMove = move      
        return bestMove 
        
        """
        legalMoves=gameState.getLegalActions(0)
        #print "LeaglMovews:",legalMoves
        scores=[self.getValue(gameState.generateSuccessor(0,move),1,1) for move in legalMoves]
        #print "scores:",scores
        bestScore=max(scores)
        #print "bestScore:",max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        #print "bestIndices:", bestIndices
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best
        #print "chosenIndex:",chosenIndex
        #print "Moves:",legalMoves[chosenIndex]
        return legalMoves[chosenIndex]
       """

    def getValue(self, gameState, agentIndex, currentDepth):  #this is a rescurise call for it call from root to leaf
        if gameState.isWin() or gameState.isLose() or currentDepth>= gameState.getNumAgents() * self.depth:
           
           #print gameState
           return self.evaluationFunction(gameState)
        if agentIndex==0:
           
           #print gameState
           return self.getMax(gameState, agentIndex, currentDepth)
        else:
           
           #print gameState
           return self.getMin(gameState, agentIndex, currentDepth)
    
    def getMax(self, gameState,agentIndex, currentDepth):
        legalMoves=gameState.getLegalActions(agentIndex) #current agent's legal action moves
        value=float('-inf')
        for move in legalMoves:
            successorState=gameState.generateSuccessor(agentIndex,move)
            successorDepth=currentDepth+1
            #value=max(value,self.evaluationFunction(gameState))
            value = max(value, self.getValue(successorState, successorDepth % gameState.getNumAgents(), successorDepth))
            #print value
        return value

    def getMin(self, gameState,agentIndex, currentDepth):
        legalMoves=gameState.getLegalActions(agentIndex) #current agent's legal action moves
        value=float('inf')
        for move in legalMoves:
            successorState=gameState.generateSuccessor(agentIndex,move)
            successorDepth=currentDepth+1
            #value=min(value,self.evaluationFunction(gameState))
            value = min(value, self.getValue(successorState, successorDepth % gameState.getNumAgents(), successorDepth))
            #print value
        return value
    
    



class AlphaBetaAgent(MultiAgentSearchAgent):

    """
      Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState):
        
          #Returns the minimax action using self.depth and self.evaluationFunction
       
        legalMoves = gameState.getLegalActions(0)
        bestMove= ''
        value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in legalMoves:
            tempValue = self.getValue(gameState.generateSuccessor(0, move), 1 % gameState.getNumAgents(), 1, alpha, beta)
            if  value < tempValue :
                value = tempValue
                bestMove = move
                if beta < value:
                    return bestMove
                alpha = max(alpha, value)
        return bestMove 
       

    def getValue(self, gameState, agentIndex, currentDepth,alpha,beta):  #this is a rescurise call for it call from root to leaf
        if gameState.isWin() or gameState.isLose() or currentDepth>= gameState.getNumAgents() * self.depth:
           
           #print gameState
           return self.evaluationFunction(gameState)
        if agentIndex==0:
           
           #print gameState
           return self.getMax(gameState, agentIndex, currentDepth,alpha,beta)
        else:
           
           #print gameState
           return self.getMin(gameState, agentIndex, currentDepth,alpha,beta)
    
    def getMax(self, gameState,agentIndex, currentDepth,alpha,beta):
        legalMoves=gameState.getLegalActions(agentIndex) #current agent's legal action moves
        value=float('-inf')
        for move in legalMoves:
            successorState=gameState.generateSuccessor(agentIndex,move)
            successorDepth=currentDepth+1
            #value=max(value,self.evaluationFunction(gameState))
            value = max(value, self.getValue(successorState, successorDepth % gameState.getNumAgents(), successorDepth,alpha,beta))
            #print value
            if value>beta:
              return value
            alpha=max(alpha,value)
        return value

    def getMin(self, gameState,agentIndex, currentDepth,alpha,beta):
        legalMoves=gameState.getLegalActions(agentIndex) #current agent's legal action moves
        value=float('inf')
        for move in legalMoves:
            successorState=gameState.generateSuccessor(agentIndex,move)
            successorDepth=currentDepth+1
            #value=min(value,self.evaluationFunction(gameState))
            value = min(value, self.getValue(successorState, successorDepth % gameState.getNumAgents(), successorDepth,alpha,beta))
            #print value
            if value<alpha:
              return value
            beta =min(beta,value)
        return value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        legalMoves=gameState.getLegalActions(0)
        bestScore=float("-inf")
        bestMove=''
        for move in legalMoves:
            tempScore = self.getValue(gameState.generateSuccessor(0, move), 1 , 1)
            if  bestScore < tempScore :
                bestScore = tempScore
                bestMove = move      
        return bestMove 

    def getValue(self,gameState,agentIndex,currentDepth):
        if currentDepth >= gameState.getNumAgents()*self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.getMax(gameState, agentIndex, currentDepth)
        else:
            return self.getExpected(gameState, agentIndex, currentDepth)

    def getMax(self, gameState,agentIndex, currentDepth):
        legalMoves=gameState.getLegalActions(agentIndex) #current agent's legal action moves
        value=float('-inf')
        for move in legalMoves:
            successorState=gameState.generateSuccessor(agentIndex,move)
            successorDepth=currentDepth+1
            #value=max(value,self.evaluationFunction(gameState))
            value = max(value, self.getValue(successorState, successorDepth % gameState.getNumAgents(), successorDepth))
            #print value
        return value

    def getExpected(self, gameState,agentIndex, currentDepth):
        legalMoves=gameState.getLegalActions(agentIndex) #current agent's legal action moves
        values=[]
        for move in legalMoves:
            successorState=gameState.generateSuccessor(agentIndex,move)
            successorDepth=currentDepth+1
            #value=min(value,self.evaluationFunction(gameState))
            value = self.getValue(successorState, successorDepth % gameState.getNumAgents(), successorDepth)
            #print value
            values.append(value)
        return sum(values)*1.0 / len(values)
      
def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 4).

      DESCRIPTION: <I just consider of the evalution above and think of how to add the food score 
      cobsideration and the scaredScore about the ghost's scaredTime>
    """

    PacmanPosition=currentGameState.getPacmanPosition()
    food=currentGameState.getFood()
    ghostStates=currentGameState.getGhostStates()
    scaredTimes=[ghostState.scaredTimer for ghostState in ghostStates]
    #print "pos:", pos
    #print "food",food
    #print "ghostSates:",ghostStates
    #print "scaredTimes:",scaredTimes


    foodList=food.asList()
    closestFood = foodList and min([util.manhattanDistance(PacmanPosition, foodPos) for foodPos in foodList]) or 0
    foodScore = closestFood and 1.0 / float(closestFood)
    closestGhostDist = min([util.manhattanDistance(PacmanPosition, ghostState.getPosition()) for ghostState in ghostStates])
    scaredScore = sum(scaredTimes)
        
    return currentGameState.getScore() + sum([foodScore * closestGhostDist, scaredScore])

      
# Abbreviation
better = betterEvaluationFunction

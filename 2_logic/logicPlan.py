# logicPlan.py
# ------------
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


"""
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    "util.raiseNotDefined()"
    A=logic.Expr('A')
    B=logic.Expr('B')
    C=logic.Expr('C')
    symbol1=A|B
    symbol2=(~A)%((~B)|C)
    symbol3=logic.disjoin([(~A),(~B),C])
    symbol=logic.conjoin([symbol1,symbol2,symbol3])
    return symbol


def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A=logic.Expr('A')
    B=logic.Expr('B')
    C=logic.Expr('C')
    D=logic.Expr('D')
    symbol1=C%(B|D)
    symbol2=A>>((~B)&(~D))
    symbol3=(~(B&(~C)))>>A
    symbol4=(~D)>>C
    symbol=logic.conjoin([symbol1,symbol2,symbol3,symbol4])
    return symbol
    

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    WumpusAlive1=logic.PropSymbolExpr('WumpusAlive',1)
    WumpusAlive0=logic.PropSymbolExpr('WumpusAlive',0)
    WumpusBorn0=logic.PropSymbolExpr('WumpusBorn',0)
    WumpusKilled0=logic.PropSymbolExpr('WumpusKilled',0)
    symbol1=WumpusAlive1%((WumpusAlive0&(~WumpusKilled0))|((~WumpusAlive0)&WumpusBorn0))
    symbol2=~(WumpusAlive0&WumpusBorn0)
    symbol3=WumpusBorn0
    symbol=logic.conjoin([symbol1,symbol2,symbol3])
    return symbol

def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    return logic.pycoSAT(logic.to_cnf(sentence))

def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    return logic.disjoin(literals)


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    """
    Never exist two expr is true
    for example literals=[A,B,C], we return (~A|~B)&(~A|~C)&(~B|~C)
    """
    symbols=[]
    results=[]
    for symbol in literals:
        symbols.append(~symbol)
    for i in range(0,len(literals)-1):
        for j in range(i+1,len(literals)):
            results.append((symbols[i]|symbols[j]))
    return logic.conjoin(results)

def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    return logic.conjoin(atLeastOne(literals),atMostOne(literals))


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    """
    for m in model:
        print m," ",logic.PropSymbolExpr.parseExpr(m)[0]," ",logic.PropSymbolExpr.parseExpr(m)[1]

    parseExpr(m)[0] will return the action, paeseExpr(m)[1] will return the specific indices value
    for example "North[3]"=> "North"   3,   P[3,4,1]=> "P", (3,4,1)
    """

    actionsMove=[]
    times=[]

    "Get the legal actionsMoves and Times"
    for m in model:
        if  (logic.PropSymbolExpr.parseExpr(m)[0] in actions) and model[m]:
            actionsMove.append(logic.PropSymbolExpr.parseExpr(m)[0])
            times.append(logic.PropSymbolExpr.parseExpr(m)[1])
   
    "Sort the actionMoves in time order"    
    for i in range(0,len(times)-1):
        for j in range(i+1,len(times)):
            if int(times[i])>int(times[j]):
                temp1=times[j]
                times[j]=times[i]
                times[i]=temp1
                temp2=actionsMove[j]
                actionsMove[j]=actionsMove[i]
                actionsMove[i]=temp2


    return actionsMove

def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    "return logic.Expr('A') # Replace this with your expression"
    legalMoves=[]
    if not walls_grid[x+1][y]:
        legalMoves.append(logic.PropSymbolExpr(pacman_str,x+1,y,t-1)&logic.PropSymbolExpr('West',t-1))
    if not walls_grid[x-1][y]:
        legalMoves.append(logic.PropSymbolExpr(pacman_str,x-1,y,t-1)&logic.PropSymbolExpr('East',t-1))
    if not walls_grid[x][y+1]:
        legalMoves.append(logic.PropSymbolExpr(pacman_str,x,y+1,t-1)&logic.PropSymbolExpr('South',t-1))
    if not walls_grid[x][y-1]:
        legalMoves.append(logic.PropSymbolExpr(pacman_str,x,y-1,t-1)&logic.PropSymbolExpr('North',t-1))

    return logic.PropSymbolExpr(pacman_str,x,y,t)%(logic.disjoin(legalMoves))
    


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    
    "*** YOUR CODE HERE ***"
    #First, we need to get the start and goal position
    start=problem.getStartState()
    goal=problem.getGoalState()

    #Secondly, we need define a logic expression list to store the logic expression, which is used to make the model  
    expressions=[]

    #Thirdly, we need to initialize our logic expressions at time=0, 
    #now every (x,y) position is not moved except start position, and we can get an exactly one action in time 0
    expressions = [logic.PropSymbolExpr(pacman_str,start[0],start[1],0)]
    for x in range(1,width+1):
        for y in range(1,height+1):
            if not walls[x][y] and (x != start[0] or y != start[1]):
                expressions.append(~logic.PropSymbolExpr(pacman_str,x,y,0))

    expressions.append(exactlyOne([logic.PropSymbolExpr('East',0), logic.PropSymbolExpr('West',0),logic.PropSymbolExpr('South',0),logic.PropSymbolExpr('North',0)]))

    #Finally, we need to find our solution in no more than 50 steps, it's similar to time=0, 
    #but with time plus 1, we need to use the expressions to construct a model and try to extract a action moves from the model
    for t in range(1,51):
        for x in range(1,width+1):
            for y in range(1,height+1):
                if not walls[x][y]:
                    expressions.append(pacmanSuccessorStateAxioms(x,y,t,walls))
        expressions.append(exactlyOne([logic.PropSymbolExpr('East',t), logic.PropSymbolExpr('West',t),logic.PropSymbolExpr('South',t),logic.PropSymbolExpr('North',t)]))
        expressions.append(pacmanSuccessorStateAxioms(goal[0],goal[1],t+1,walls))
        expressions.append(logic.PropSymbolExpr(pacman_str,goal[0],goal[1],t+1))
        model=findModel(logic.conjoin(expressions))
        
        if model:
            actions = ['North', 'South', 'East', 'West']
            return extractActionSequence(model, actions)
            
        expressions.pop()
        expressions.pop()



def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()

    "*** YOUR CODE HERE ***"
    """
      A planning state in FoodPlanningProblem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """

    #I solve prpblem 6 is just similar to problem 5
    #Firstly, get the start satte and the foodGrid
    startState=problem.getStartState()
    start = startState[0]
    foodGrid=startState[1]
    #print "start:",start
    #print "foodGrid:",foodGrid

    #Secondly, we need defibe a logic expression list to store the logic expression, which is used to make the model  
    expressions=[]

    #Thirdly, we need to initialize our logic expressions at time=0, 
    #now every (x,y) position is not moved except start position, and we can get an exactly one action in time 0
    expressions = [logic.PropSymbolExpr(pacman_str,start[0],start[1],0)]
    for x in range(1,width+1):
        for y in range(1,height+1):
            if not walls[x][y] and (x != start[0] or y != start[1]):
                expressions.append(~logic.PropSymbolExpr(pacman_str,x,y,0))
    expressions.append(exactlyOne([logic.PropSymbolExpr('East',0), logic.PropSymbolExpr('West',0),logic.PropSymbolExpr('South',0),logic.PropSymbolExpr('North',0)]))
    
    #Finally, we need to find our solution in no more than 50 steps, it's similar to time=0,
    #but with time plus 1, we need to use the expressions to construct a model and try to extract a action moves from the model
    for t in range(1,51):
        for x in range(1,width+1):
            for y in range(1,height+1):
                if not walls[x][y]:
                    expressions.append(pacmanSuccessorStateAxioms(x,y,t,walls))
        expressions.append(exactlyOne([logic.PropSymbolExpr('East',t), logic.PropSymbolExpr('West',t),logic.PropSymbolExpr('South',t),logic.PropSymbolExpr('North',t)]))
        
        #So far, we're similar to problem 5, and next we need to add the food logic to the expressions
        count = 0 #record the food logic I have added in the expressions at time t       
        for x in range(1,width+1):
            for y in range(1,height+1):
                visit = []
                if foodGrid[x][y]: #for every food, we need to record a visit when I can eat it in time i
                    for i in range(1,t+1):
                        visit.append(logic.PropSymbolExpr(pacman_str,x,y,i))
                    expressions.append(atLeastOne(visit))
                    count += 1

        model=findModel(logic.conjoin(expressions))
        if model:
            actions = ['North', 'South', 'East', 'West']
            return extractActionSequence(model, actions)
        #Before we go into next time t+1, we need to delete the food logic in time t   
        for i in range(0,count):
            expressions.pop()


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    
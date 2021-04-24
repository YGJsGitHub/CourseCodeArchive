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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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

        "*** YOUR CODE HERE ***"
        food = currentGameState.getFood()
        sucPos = list(successorGameState.getPacmanPosition())
        score = float("-inf")

        foodList = food.asList()

        if action == 'Stop':
            return score

        for ghostState in newGhostStates:
            if ghostState.getPosition() == tuple(sucPos) and (ghostState.scaredTimer == 0):
                return score

        for food in foodList:
            tmpDistance = -manhattanDistance(sucPos, food)
            if (tmpDistance > score):
                score = tmpDistance

        return score

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
    Your minimax agent (question 2)
    """
    def minValue(self, gameState, agent, depth):
        current_best_value = float("inf")  # highest possible value
        # loop through all the legal actions of the agent (pacman or ghosts)
        for action in gameState.getLegalActions(agent):
            suc = gameState.generateSuccessor(agent, action)  # successor
            value = self.minimax(suc, agent + 1, depth)
            # pick the min of current best and value
            current_best_value = min(current_best_value, value)
        return current_best_value

    def maxValue(self, gameState, agent, depth):
        current_best_value = float("-inf")  # lowest possible value
        # loop through all the legal actions of the agent (pacman or ghosts)
        for action in gameState.getLegalActions(agent):
            suc = gameState.generateSuccessor(agent, action)  # successor
            # check for the next agent
            value = self.minimax(suc, agent + 1, depth)
            # pick the max of current best and value
            current_best_value = max(current_best_value, value)
            # Final action, that performs at depth 1, is saved
            if depth == 1 and current_best_value == value:
                self.action = action
        return current_best_value

    def minimax(self, gameState, agent=0, depth=0):
        # to keep the agent index in range, we can get modules of number of agents, then we can increment the agent index by one
        agent = agent % gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if agent == 0:  # maximize for pacman
            # calculate the next agent and increment the depth accordingly
            if depth < self.depth:
                return self.maxValue(gameState, agent, depth+1)
            else:
                return self.evaluationFunction(gameState)
        else:  # minimize for ghosts
          return self.minValue(gameState, agent, depth)

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
        """
        "*** YOUR CODE HERE ***"
        self.minimax(gameState)
        return self.action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def minValue(self, gameState, depth, agent, a, b):
        minimum = ["", float("inf")]

        for action in gameState.getLegalActions(agent):
            suc = gameState.generateSuccessor(agent, action)
            value = self.miniMax(suc, depth, agent + 1, a, b)

            if type(value) is not list:
                newVal = value
            else:
                newVal = value[1]

            if newVal < minimum[1]:
                minimum = [action, newVal]
            if newVal < a:
                return [action, newVal]
            b = min(b, newVal)
        return minimum

    def maxValue(self, gameState, depth, agent, a, b):
        maximum = ["", -float("inf")]

        for action in gameState.getLegalActions(agent):
            suc = gameState.generateSuccessor(agent, action)
            value = self.miniMax(suc, depth, agent + 1, a, b)

            if type(value) is not list:
                newVal = value
            else:
                newVal = value[1]

            # real logic
            if newVal > maximum[1]:
                maximum = [action, newVal]
            if newVal > b:
                return [action, newVal]
            a = max(a, newVal)
        return maximum

    def miniMax(self, gameState, depth, agent, a, b):
        if agent >= gameState.getNumAgents():
            depth += 1
            agent = 0

        if (depth == self.depth or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        elif (agent == 0):
            return self.maxValue(gameState, depth, agent, a, b)
        else:
            return self.minValue(gameState, depth, agent, a, b)


    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        actionsList = self.miniMax(gameState, 0, 0, -float("inf"), float("inf"))
        return actionsList[0]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def expectFinder(self, gameState, depth, agentcounter):
        expectimax = ["", 0]
        ghostActions = gameState.getLegalActions(agentcounter)
        probability = 1.0 / len(ghostActions)

        if not ghostActions:
            return self.evaluationFunction(gameState)

        for action in ghostActions:
            suc = gameState.generateSuccessor(agentcounter, action)
            value = self.expectimant(suc, depth, agentcounter + 1)
            if type(value) is list:
                newVal = value[1]
            else:
                newVal = value
            expectimax[0] = action
            expectimax[1] += newVal * probability
        return expectimax

    def maxValue(self, gameState, depth, agentcounter):
        maximum = ["", -float("inf")]
        actions = gameState.getLegalActions(agentcounter)

        if not actions:
            return self.evaluationFunction(gameState)

        for action in actions:
            suc = gameState.generateSuccessor(agentcounter, action)
            value = self.expectimant(suc, depth, agentcounter + 1)
            if type(value) is not list:
                newVal = value
            else:
                newVal = value[1]
            if newVal > maximum[1]:
                maximum = [action, newVal]
        return maximum

    def expectimant(self, gameState, depth, agentcounter):
        if agentcounter >= gameState.getNumAgents():
            depth += 1
            agentcounter = 0

        if depth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        elif (agentcounter == 0):
            return self.maxValue(gameState, depth, agentcounter)
        else:
            return self.expectFinder(gameState, depth, agentcounter)

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # All work and no play makes Jason a dull boy
        # All work and no play makes Jason a dull boy
        # All work and no play makes Jason a dull boy
        # All work and no play makes Jason a dull boy
        # All work and no play makes Jason a dull boy
        # All work and no play makes Jason a dull boy
        # All work and no play makes Jason a dull boy
        # All work and no play makes Jason a dull boy
        # All work and no play makes Jason a dull boy
        # All work and no play makes Jason a dull boy
        # All work and no play makes Jason a dull boy
        # All work and no play makes Jason a dull boy
        # All work and no play makes Jason a dull boy
        # All work and no play makes Jason a dull boy
        actionsList = self.expectimant(gameState, 0, 0)
        return actionsList[0]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    position = list(currentGameState.getPacmanPosition())
    foodList = currentGameState.getFood().asList()
    scoreList = []

    for food in foodList:
        scoreList.append(-manhattanDistance(position, food))

    if not scoreList:
        scoreList.append(0)

    bestscore = max(scoreList)

    return currentGameState.getScore() + bestscore

# Abbreviation
better = betterEvaluationFunction

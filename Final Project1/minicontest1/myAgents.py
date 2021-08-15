# myAgents.py
# ---------------
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

from game import Agent, Directions
from searchProblems import PositionSearchProblem, manhattanHeuristic

import util
import time
import search

"""
IMPORTANT
`agent` defines which agent you will use. By default, it is set to ClosestDotAgent,
but when you're ready to test your own agent, replace it with MyAgent
"""
def createAgents(num_pacmen, agent='MyAgent'):
    return [eval(agent)(index=i) for i in range(num_pacmen)]

class MyAgent(Agent):
    """
    Implementation of your agent.
    """
    #각 pacman이 어디로 이동하는 지 저장하는 list이다. 
    #index를 이용하여 각 pacman이 어디로 이동하는 지 알 수 있다.
    GoingList = [(-1,-1)] * 15
    #각 pacman의 계획된 움직임들을 담은 list이다. 
    actionList = [0] *15
    #각 pacman의 actionList의 길이를 담은 list이다.
    actionLength = [0] * 15
    #Agent의 개수를 저장한 변수이다.
    agentNum = 0

    def getAction(self, state):
        """
        Returns the next action the agent will take
        """

        "*** YOUR CODE HERE ***"
        #curFood에 음식의 정보들을 저장한다.
        curFood = state.getFood()
        #problem에 밑에서 정의한 AnyFoodSearchProblem으로 저장한다.
        problem = AnyFoodSearchProblem(state, self.index)
        
        #agentNum이 짝수라면 2로 나눈 몫을 n으로 저장한다.
        if MyAgent.agentNum%2==0:
            n = MyAgent.agentNum/2
        #짝수가 아니라면 2로 나눈 몫+1을 n으로 저장한다.
        else:
            n = MyAgent.agentNum/2+1   

        #pacman의 actionList가 비어있는 list일 경우(actionLength가 0일 경우) 
        #BFS의 방식을 사용한다.
        if MyAgent.actionLength[self.index]==0:
            #처음 상태와 일련의 action들을 담을 list를 원소로 가지는 튜플을 pacmanCurrent이라고 하였다.
            pacmanCurrent = (problem.getStartState(), [])
            #방문했던 위치를 저장할 visitedPosition을 set으로 선언하였다.
            visitedPosition = set()
            #BFS에 사용될 Queue를 선언하였다.
            fringe = util.Queue()
            #fringe에 pacmanCurrent를 넣는다.
            fringe.push(pacmanCurrent)
            
            #fringe가 비어있지 않을 경우 반복문을 반복한다.
            while not fringe.isEmpty():
                #Queue에서 원소를 꺼내고 그것을 pacmanCurrent라고 하자.
                pacmanCurrent = fringe.pop()
                #만약 pacmanCurrent[0]이 이미 방문했던 위치라면 while문의 처음으로 돌아간다.(continue)
                if pacmanCurrent[0] in visitedPosition:
                    continue
                #pacmanCurrent[0]이 이미 방문했던 위치가 아니라면.
                else:
                    #pacmanCurrent[0]을 visitedPosition에 추가한다.
                    visitedPosition.add(pacmanCurrent[0])
                #만약 pacmanCurrent[0]이 도착위치라면(Food라면)
                if problem.isGoalState(pacmanCurrent[0]):
                    #만약 현재 남은 음식의 개수가 agent의 절반(홀수일 경우 절반+1)보다 작을 경우
                    if len(curFood.asList())<=n:
                        #현재 탐색중인 pacman agent의 GoingList에 찾은 goal의 위치를 대입한다.
                        MyAgent.GoingList[self.index] = pacmanCurrent[0]
                        #actionList에 pacmanCurrent[1]을 대입한다.
                        MyAgent.actionList[self.index] = pacmanCurrent[1]
                        #actionLength에 actionList의 길이를 대입한다.
                        MyAgent.actionLength[self.index] = len(MyAgent.actionList[self.index])
                        break
                    #뒤에서 case를 분류하기 위해 사용될 변수 flag1, flag2를 False로 초기화한다.
                    flag1 = False
                    flag2 = False
                    #GoingList를 돌면서 지금 pacman agent가 찾은 goal과 같은 goal로 향하고 있는 다른 pacman agent가 있는지 확인한다.
                    for my_goal_index,k in enumerate(MyAgent.GoingList):
                        #만약 같은 goal로 향하고 있는 다른 pacman agent가 있다면
                        if k[0] == pacmanCurrent[0][0] and k[1]==pacmanCurrent[0][1]:
                            #이때 다른 pacman agent의 actionLength가 현재 탐색중인 pacman agent의 actionLength보다 크다면 
                            if MyAgent.actionLength[my_goal_index]>len(pacmanCurrent[1]):
                                #다른 Pacman agent의 GoingList를 (-1,-1)로 바꿔준다.
                                MyAgent.GoingList[my_goal_index]=(-1,-1)
                                #actionList도 빈 list로 바꿔준다.
                                MyAgent.actionList[my_goal_index] = []
                                #actionLength도 0으로 바꿔준다.
                                MyAgent.actionLength[my_goal_index] = 0
                                #현재 탐색중인 pacman agent의 GoingList에 찾은 goal의 위치를 대입한다.
                                MyAgent.GoingList[self.index] = pacmanCurrent[0]
                                #actionList에 pacmanCurrent[1]을 대입한다.
                                MyAgent.actionList[self.index] = pacmanCurrent[1]
                                #actionLength에 actionList의 길이를 대입한다.
                                MyAgent.actionLength[self.index] = len(MyAgent.actionList[self.index])
                                #flag2를 True로 바꿔준다.
                                flag2 = True
                            #flag1을 True로 바꿔준다.
                            flag1 = True
                                
                    #다른 pacman agent와 goal은 겹쳤지만, 현재 탐색중인 pacman agent의 actionLength가 더 작은 경우가 있었을 경우
                    if flag1==True and flag2 == True:
                        break
                    #다른 pacman agent와 goal은 겹쳤지만, 현재 탐색중인 pacman agent의 actionLength가 더 작은 경우가 없었을 경우
                    elif flag1==True and flag2 == False:    
                        #현재 방문 장소를 visitedPosition에 추가한다.
                        visitedPosition.add(pacmanCurrent[0])
                        #continue를 이용하여 while문 처음으로 돌아가 탐색을 계속한다. 
                        continue
                    #다른 pacman agent와 goal이 겹치지 않았을 경우
                    else:
                        #현재 탐색중인 pacman agent의 GoingList에 찾은 goal의 위치를 대입한다.    
                        MyAgent.GoingList[self.index] = pacmanCurrent[0]
                        #actionList에 pacmanCurrent[1]을 대입한다.
                        MyAgent.actionList[self.index] = pacmanCurrent[1]
                        #actionLength에 actionList의 길이를 대입한다.
                        MyAgent.actionLength[self.index] = len(MyAgent.actionList[self.index])
                        #탐색을 중지한다.
                        break
                
                #pacmanCurrent[0]이 goal이 아닐 경우
                else:
                    #다음 상태를 getSuccessors함수를 이용하여 얻는다.
                    pacmanSuccessors = problem.getSuccessors(pacmanCurrent[0])
                #pacmanSuccessors에 대해 반복문을 돌면서 탐색을 수행한다.
                for item in pacmanSuccessors:  
                    #만약 item[0](pacman의 다음 위치)가 visitedPosition에 없다면(방문했던 위치가 아니라면)
                    if item[0] not in visitedPosition:
                        #pacmanRoute에 pacmanCurrent[1]을 복사한 것을 대입한다.
                        pacmanRoute = pacmanCurrent[1].copy()
                        #pacmanRoute에 item[1](다음 위치로의 행동)을 추가한다.
                        pacmanRoute.append(item[1])
                        #fringe에 (다음위치, pacmanRoute)를 넣는다.
                        fringe.push((item[0], pacmanRoute))

        #만약 actionList의 길이가 0보다 작다면
        if len(MyAgent.actionList[self.index])<=0:
            #다음 행동으로 STOP를 명령한다.
            return Directions.STOP
        #actionList의 길이가 0보다 크다면
        else:
            #actionList의 첫 번째 원소를 다음 act으로 지정한다.
            act = MyAgent.actionList[self.index][0]
            #기존 actionList에서 첫 번째 원소를 제거한다.
            MyAgent.actionList[self.index] = MyAgent.actionList[self.index][1:]
            #actionLength를 1 감소시킨다.
            MyAgent.actionLength[self.index] = MyAgent.actionLength[self.index]-1
            #만약 actionLength가 0이 되었다면
            if MyAgent.actionLength[self.index]==0:
                #GoingList를 (-1,-1)로 초기화한다.
                MyAgent.GoingList[self.index] == (-1,-1)
            #act(다음 action)를 반환한다.
            return act

    def initialize(self):
        """
        Intialize anything you want to here. This function is called
        when the agent is first created. If you don't need to use it, then
        leave it blank
        """

        "*** YOUR CODE HERE"
        #agent가 생성될때마다 agentNum을 하나씩 증가시킨다.
        MyAgent.agentNum = MyAgent.agentNum+1
"""
Put any other SearchProblems or search methods below. You may also import classes/methods in
search.py and searchProblems.py. (ClosestDotAgent as an example below)
"""

class ClosestDotAgent(Agent):

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition(self.index)
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState, self.index)


        "*** YOUR CODE HERE ***"

        pacmanCurrent = [problem.getStartState(), [], 0]
        visitedPosition = set()
        # visitedPosition.add(problem.getStartState())
        fringe = util.PriorityQueue()
        fringe.push(pacmanCurrent, pacmanCurrent[2])
        while not fringe.isEmpty():
            pacmanCurrent = fringe.pop()
            if pacmanCurrent[0] in visitedPosition:
                continue
            else:
                visitedPosition.add(pacmanCurrent[0])
            if problem.isGoalState(pacmanCurrent[0]):
                return pacmanCurrent[1]
            else:
                pacmanSuccessors = problem.getSuccessors(pacmanCurrent[0])
            Successor = []
            for item in pacmanSuccessors:  # item: [(x,y), 'direction', cost]
                if item[0] not in visitedPosition:
                    pacmanRoute = pacmanCurrent[1].copy()
                    pacmanRoute.append(item[1])
                    sumCost = pacmanCurrent[2]
                    Successor.append([item[0], pacmanRoute, sumCost + item[2]])
            for item in Successor:
                fringe.push(item, item[2])
        return pacmanCurrent[1]

    def getAction(self, state):
        return self.findPathToClosestDot(state)[0]

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState, agentIndex):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition(agentIndex)
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state
        if self.food[x][y] == True:
            return True
        return False


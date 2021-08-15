# myTeam.py
# ---------
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


from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'attack', second = 'defense'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class PlanningCaptureAgent(CaptureAgent):
  """
  A base class for reflex agents that chooses score-maximizing actions
  """
 
  def registerInitialState(self, gameState):
    #처음 출발 위치를 start에 저장
    self.start = gameState.getAgentPosition(self.index)
    #상대 팀원들의 index를 받아서 opponents에 저장
    self.opponents = self.getOpponents(gameState)
    #우리 팀원들의 index를 받아서 teams에 저장
    self.teams = self.getTeam(gameState)
    #이 클래스는 CaptureAgent를 상속했으므로, CaptureAgent의 초기화함수를 호출해준다.
    CaptureAgent.registerInitialState(self, gameState)
    

  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """   
    #현재 탐색 중인 agent가 취할수 있는 행동을 actions에 저장 
    actions = gameState.getLegalActions(self.index)

    #현재 남은 음식의 개수가 2보다 작을 경우
    if len(self.getFood(gameState).asList())<=2:
      #출발점과의 최소 거리를 bestDist라고 선언하고 초기값을 infinity로 지정
      bestDist=float('inf')
      #가능한 행동들 사이에서 출발점과 가장 가까운 곳으로 가는 행동을 찾는다.
      for action in actions:
        #action을 취했을 때 도달하는 상태를 successor에 저장
        successor = gameState.generateSuccessor(self.index,action)
        #successor의 위치를 pos2에 저장
        pos2 = successor.getAgentPosition(self.index)
        #출발점과 pos2사이의 거리를 dist에 저장
        dist = self.getMazeDistance(self.start,pos2)
        #만약 dist가 bestDist보다 작다면 (최소값을 구하는 과정)
        if dist<bestDist:
          #그때의 action을 bestAct에 저장한다.
          bestAct = action
          #그때의 거리를 bestDist라고 한다.
          bestDist = dist
      #최종적으로 선택된 bestAct를 반환한다.
      return bestAct
    #현재 남은 음식의 개수가 2보다 클 경우
    else:
      #getAction에서 받은 행동을 bestAction에 저장
      bestAction = self.getAction(gameState)
      #bestAction을 반환한다.
      return bestAction

  #minimax와 alpha-beta pruning을 사용
  #max노드에서의 행동에 대한 함수(max_value)를 정의한다.
  def max_value(self,gameState, depth, a, b):
    #만약 현재 depth가 2라면 evaluate의 값을 반환한다.
    if depth == 2:
        return self.evaluate(gameState)

    #최댓값을 구해야 하므로 v를 -infinity로 선언해준다.
    v = float('-inf')
    #각각의 successor에 대해 v의 최댓값을 구해준다.
    for action in gameState.getLegalActions(self.index):
        #가능한 actions 중 action을 취했을 때 도달하는 상태를 successor이라고 하자.
        successor = gameState.generateSuccessor(self.index,action)
        #minimax search이므로 min-value에서 나온 값들 중 최댓값을 구한다.
        #이때 min-value는 첫번째 ghost부터 해야하므로 index를 self.opponents[0]으로 주고, depth는 그대로 넘겨준다.
        v = max(v, self.min_value(successor,self.opponents[0],depth, a, b))
        #만약 v가 b(beta)보다 크다면 v를 바로 반환한다.(pruning)
        if v > b:
            return v
        #현재 a(alpha)와 v중 큰 값을 a로 갱신한다.
        a = max(a,v)
    #v를 반환한다.
    return v
        
  #min노드에서의 행동에 대한 함수(min-value)를 정의한다.
  #이때 ghost마다 각각의 index가 있으므로 index도 같이 받는다.
  def min_value(self,gameState, index, depth, a, b):
    #최소값을 구해야 하므로 v를 infinity로 선언해준다.
    v = float('inf')
    #각각의 successor에 대해 v의 최소값을 구해준다.
    for action in gameState.getLegalActions(index):
      #가능한 actions 중 action을 취했을 때 도달하는 상태를 successor이라고 하자.
      successor = gameState.generateSuccessor(index,action)
      #만약 현재 ghost의 index가 마지막 index라면 다음에는 pacman에 대해 max_search가 실행되야한다.
      if index==self.opponents[1]:
        #다음 노드가 max이므로 max-value중 최소값을 구해준다.
        #이때 한 번의 탐색이 끝났으므로 depth를 1증가시킨다.
        v = min(v, self.max_value(successor,depth+1, a, b)) #beacuse of last search
      #만약 다음 탐색이 ghost에 대한 것일 경우
      else:
        #다음 노드가 min이므로 min_value중 최소값을 구해준다.
        #이때 다음 ghost의 index를 넘겨준다.
        v = min(v, self.min_value(successor,self.opponents[1],depth, a, b)) #because of not last seach
        #만약 v가 a(alpha)보다 작다면 v를 바로 반환한다.(pruning)
      if v<a:
        return v
      #현재 b(beta)와 v중 작은 값을 b로 갱신한다.
      b = min(b, v)
    #v를 반환한다.
    return v

  #위에서 작성한 함수를 토대로 action을 반환하는 getAction함수를 정의
  def getAction(self,gameState):
    #현재 탐색 대상(나)인 agent가 가지고있는 음식의 개수를 havingFood에 저장
    havingFood = gameState.getAgentState(self.index).numCarrying
    #남은 음식들을 list의 형태로 foodLeft에 저장
    foodLeft = self.getFood(gameState).asList()
    #현재 탐색 대상(나)인 agent의 위치를 pos에 저장
    pos = gameState.getAgentPosition(self.index)
    
    #음식까지의 가장 작은 거리를 1000으로 저장
    minFDist = 1000

    #만약 남은 음식이 있다면
    if len(foodLeft) > 0:
      #minFDist를 구해준다.
      minFDist = min([self.getMazeDistance(pos, food) for food in foodLeft])

    #만약 현재 가지고있는 음식이 5개 이상이고, 주변에 음식이 없다면
    if (havingFood>=5 and minFDist>1):
      #출발점까지의 거리를 9999로 초기화한다음 bestDist에 저장
      bestDist = 9999
      #가능한 행동들 사이에서 출발점과 가장 가까운 곳으로 가는 행동을 찾는다.
      for action in gameState.getLegalActions(self.index):
        #action을 취했을 때 도달하는 상태를 successor에 저장
        successor = self.getSuccessor(gameState, action)
        #successor의 위치를 pos2에 저장
        pos2 = successor.getAgentPosition(self.index)
        #출발점과 pos2사이의 거리를 dist에 저장
        dist = self.getMazeDistance(self.start,pos2)
        #만약 dist가 bestDist보다 작다면 (최소값을 구하는 과정)
        if dist < bestDist:
          #그때의 action을 bestAction에 저장한다.
          bestAction = action
          #그때의 거리를 bestDist라고 한다.
          bestDist = dist
      #최종적으로 선택된 bestAction를 반환한다.
      return bestAction

    #pacman이 움직여야 할 방향을 minimax_action이라고 선언하고 0으로 초기화하였다.
    minimax_action = 0
    
    #minimax_value의 최댓값을 구하고 그 값에 해당하는 노드로 이동할 것이다.
    #이때 최댓값을 구해야하므로 minimax_value를 -infinity로 초기화하였다.
    #a(alpha)를 -infinity로, b(beta)를 infinity로 초기화하였다.
    minimax_value = float('-inf')
    a = float('-inf')
    b = float('inf')
    #depth = 0에서 pacman의 다음 노드중에서 값이 가장 높은 것을 찾는다.
    for action in gameState.getLegalActions(self.index):
        #가능한 actions 중 action을 취했을 때 도달하는 상태를 successor이라고 하자.
        successor = gameState.generateSuccessor(self.index,action)
        #팩맨의 다음 노드는 1번 ghost이므로 self.opponents[0] 인덱스를 가지는 ghost 대해 min_value를 구한다.
        #구한 값을 val이라고 하자. 
        val = self.min_value(successor, self.opponents[0], 0, a, b)
        #val들 중 최댓값을 구하고, 그때의 action을 minimax_action에 저장한다.
        if minimax_value <val:
            minimax_action = action
            minimax_value = val
        #a를 갱신해주어 pruning이 가능하게 한다.
        a = max(a,minimax_value)
    #minimax_action을 반환한다.
    return minimax_action
  
  #getAction에서 각 상태를 평가할 때 사용될 값을 반환할 evaluate함수 정의
  def evaluate(self, gameState):
    #getFeatures에서 값을 받아서 val에 저장
    val = self.getFeatures(gameState)
    #val을 반환
    return val
  
  #grid position에 있는 successor를 반환하는 getSuccessor함수 정의
  def getSuccessor(self, gameState, action):
    #action을 취했을때의 successor를 successor변수에 저장
    successor = gameState.generateSuccessor(self.index, action)
    #successor의 위치를 pos에 저장
    pos = successor.getAgentState(self.index).getPosition()
    #만약 pos가 pos와 가장 가까운 grid point에 있지 않다면
    if pos != nearestPoint(pos):
      #successor에서 한 번 더 action을 취했을 때 나오는 successor를 반환한다.
      return successor.generateSuccessor(self.index, action)
    #grid point에 있다면
    else:
      #successor를 반환한다.
      return successor


#공격을 담당하는 agent이다.
class attack(PlanningCaptureAgent):

  def registerInitialState(self, gameState):
    #이 클래스는 CaptureAgent를 상속했으므로, CaptureAgent의 초기화함수를 호출해준다.
    CaptureAgent.registerInitialState(self, gameState)
    #이 클래스는 PlanningCaptureAgent를 상속했으므로, PlanningCaptureAgent의 초기화함수를 호출해준다.
    PlanningCaptureAgent.registerInitialState(self,gameState)
    #처음 출발 위치를 start에 저장
    self.start = gameState.getAgentPosition(self.index)

  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """  
    #현재 탐색 중인 agent가 취할수 있는 행동을 actions에 저장   
    actions = gameState.getLegalActions(self.index)
    #현재 남은 음식의 개수를 foodLeft에 저장
    foodLeft = len(self.getFood(gameState).asList())

    #bestAct를 선언하고 0으로 초기화
    bestAct = 0
    #만약 음식이 2개 이하로 남았다면
    if foodLeft<=2 :
      #출발점과의 최소 거리를 bestDist라고 선언하고 초기값을 9999로 지정
      bestDist = 9999
      #가능한 행동들 사이에서 출발점과 가장 가까운 곳으로 가는 행동을 찾는다.
      for action in actions:
        #action을 취했을 때 도달하는 상태를 successor에 저장
        successor = self.getSuccessor(gameState, action)
        #successor의 위치를 pos2에 저장
        pos2 = successor.getAgentPosition(self.index)
        #출발점과 pos2사이의 거리를 dist에 저장
        dist = self.getMazeDistance(self.start,pos2)
        #만약 dist가 bestDist보다 작다면 (최소값을 구하는 과정)
        if dist < bestDist:
          #그때의 action을 bestAct에 저장한다.
          bestAct = action
          #그때의 거리를 bestDist라고 한다.
          bestDist = dist
      #최종적으로 선택된 bestAct를 반환한다.
      return bestAct
    #현재 남은 음식의 개수가 2보다 클 경우
    else:
      #getAction에서 받은 행동을 bestAction에 저장
      bestAction = self.getAction(gameState)
      #bestAction을 반환한다.
      return bestAction

  def getFeatures(self, gameState):
    #Counter로 features를 선언한다.
    features = util.Counter()

    #현재 탐색 대상인 agent(나)의 위치를 pos에 저장한다.
    pos = gameState.getAgentPosition(self.index)
    #적들의 상태를 enemies에 저장
    enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
    #적들 중 현재 상대의 영역에 있으면서 방어를 하는 ghost들의 상태를 defenders에 저장한다.
    defenders = [a for a in enemies if (a.isPacman==False) and (a.getPosition() != None)]
    
    #먹어야 할 음식을 list의 형태로 foodList에 저장한다.
    foodList = self.getFood(gameState).asList()
    #먹어야 할 capsule에 대한 정보를 capsuleList에 저장한다.
    capsuleList = self.getCapsules(gameState)
    #벽에 대한 정보를 wall에 저장한다.
    wall = gameState.getWalls()

    #numOfGhost features에 defenders의 길이를 저장한다.
    features['numOfGhost']=len(defenders)
    #nextScore features에 현재 점수를 저장한다.
    features['nextScore']=self.getScore(gameState)
    #successorScore features에 foodList의 길이를 저장한다.
    features['successorScore'] = len(foodList)
    #leftCapsules features에 capsuleList의 길이를 저장한다.
    features['leftCapsules'] = len(capsuleList)
    #canCatchN features에 0을 저장한다.
    features['canCatchN'] = 0

    #아직 pacman이 아닐때
    if gameState.getAgentState(self.index).isPacman == False:
      #적들과의 최소거리를 구한다.
      for enemy in enemies:
        dist = self.getMazeDistance(pos, enemy.getPosition())
        #만약 적과의 거리가 1보다 작거나 같다면(잡을 확률이 높다)
        if dist<=1:
          #canCatchN features에 1을 저장한다.
          features['canCatchN'] = 1

    #음식과의 최소 거리 구하기
    if len(foodList) > 0: # This should always be True,  but better safe than sorry
      minFDist = min([self.getMazeDistance(pos, food) for food in foodList])
      #음식과의 최소거리를 distanceToFood features에 저장한다.
      features['distanceToFood'] = minFDist

    #ghost와의 최소거리 구하기
    #minGDist를 선언하고 1000으로 초기화한다.
    minGDist = 1000
    #가장 가까운 ghost의 index를 minIndex라고 선언하고 0을 저장하였다.
    minIndex = 0
    #만약 defender가 있을 경우
    if len(defenders)>0:
      #가장 가까운 ghost와의 거리와 그 ghost의 index를 구한다.
      for i,defender in enumerate(defenders):
        #dist는 현재 탐색중인 agent(나)와 defender사이의 거리이다.
        dist = self.getMazeDistance(pos, defender.getPosition())
        #만약 minGDist보다 dist가 더 작을 경우
        if minGDist>dist:
          #minGDist를 dist라고 하자.
          minGDist = dist
          #minIndex를 i라고 하자.
          minIndex = i
    #distanceToGhost features에 minGDist를 저장한다.
    features['distanceToGhost'] = minGDist
    
    #적과의 거리가 1이하일때, 죽을 위기 일때
    if minGDist<=1:
      #만약 탐색중인 agent(나)가 pacman이 아니라면 상대를 잡을 수 있는 상태이다.
      if gameState.getAgentState(self.index).isPacman == False:
          #canCatch features에 5000을 저장한다.
          features['canCatch'] =5000
          #distanceToGhost featuresdp 10*minGDist를 저장하여 거리가 줄어들때 더 많은 점수가 증가하도록 하였다.
          features['distanceToGhost'] = 10*minGDist
      #탐색중인 agent(나)가 pacman이라면
      else:
        #만약 가장 가까운 defender가 scared상태이고, scaredTimer가 4보다 많이 남았다면
        if defenders[minIndex].scaredTimer>4:
          #잡을 수 있으므로 canCatch features에 5000을 저장한다.
          features['canCatch'] =5000
          #distanceToGhost features에 minGDist를 저장한다.
          features['distanceToGhost'] = minGDist
          #distanceToFood features에 2*minFDist를 저장하여 음식과의 거리에 가중치를 더 주었다.
          #ghost와의 거리보다 음식을 먹는 것에 집중하기 위함이다.
          features['distanceToFood'] = 2*minFDist
        #만약 scaredTime이 4보다 작고 0보다 클 경우
        elif defenders[minIndex].scaredTimer>0:
          #이때는 잡아야하므로, 거리가 가까워짐에 비례하여 canCatch features가 커지도록 하였다.
          features['canCatch'] = 5000*(1-minGDist)
        #만약 상대가 scared상태가 아니라면
        else:
          #도망쳐야하므로 canCatch features에 -5000을 저장한다.
          features['canCatch'] =-5000
          #ghost와의 거리가 작으면 좋지 않으므로, -7을 곱해주어 애초에 minGDist가 1보다 작거나 같은 상황을 피하도록 하였다.
          features['distanceToGhost'] = -7*minGDist

    #만약 남은 음식의 개수가 2개보다 작거나 같다면
    if len(foodList)<=2:
      #음식을 더이상 먹지 않을 것이므로 가장 가까운 음식과의 거리를 0으로 한다.
      features['distanceToFood'] = 0

    #powerCapsule
    #만약 powerCapsule의 개수가 0개보다 크다면
    if len(capsuleList)>0:
      #powerCapsule와의 최소 거리를 minCdist에 저장한다.
      minCDist = min([self.getMazeDistance(pos,capsule) for capsule in capsuleList])
      #distanceToCapsule features에 minCDist를 저장한다.
      features['distanceToCapsule'] = minCDist

    #탐색중인 agent(나)의 주변에 있는 벽의 개수를 wallNum이라고 하자.
    wallNum = 0
    #탐색해야하는 위치가 map끝이면 오류가 발생하므로 try-except문을 사용하였다.
    try:
      #만약 탐색중인 agent(나)가 pacman이라면
      if gameState.getAgentState(self.index).isPacman:  
        #내 주변의 벽을 검사하기 위해 배열 ar을 선언하였다.
        ar = [(-0.5,0),(0.5,0),(0,-0.5),(0,0.5)]
        for i in ar:
            #내 주변에 벽이 있다면
            if gameState.hasWall(pos[0]+i[0],pos[1]+i[1]):
              #wallNum을 1증가시킨다.
              wallNum = wallNum+1
    except:
      i=0
    
    #만약 주변에 벽이 3개가 있다면
    if wallNum == 3:
      #noWay features에 -1000을 저장한다.
      features['noWay'] = -1000
      #이때 내 위치에 음식이 없다면
      if self.getFood(gameState)[pos[0]][pos[1]]==False:
        #가면 안되므로 noWay features에 -1000000을 저장한다.
        features['noWay'] = -1000000

    #만약 탐색중인 agent(나)가 pacman이라면
    if gameState.getAgentState(self.index).isPacman==True:
      #가지고 있는 음식의 개수를 havingFood에 저장한다.
      havingFood = gameState.getAgentState(self.index).numCarrying
      #현재 탐색중인 agent(나)의 위치와 중앙 경계선 사이의 거리를 minHDist라고 하자.
      minHDist = abs(pos[0]-(wall.width//2)) 
      #만약 minHDist가 0이 아니라면
      if minHDist!=0:
        #having Food features에 havingFood/minHdist를 저장한다.
        #이때 가지고 있는 음식의 개수가 늘어나면 좋지만, 경계선과의 거리가 멀어지면 좋지 않으므로 이를 반영하였다.
        features['havingFood'] = havingFood/minHDist
      #만약 minHDist가 0이면
      else:
        #havingFood features에 havingFood를 저장하였다.
        features['havingFood'] = havingFood
      #만약 가지고있는 음식의 개수가 2보다 크거나 같다면
      if havingFood>=2:
        #goToHome features에 minHDist를 저장한다.
        features['goToHome'] = minHDist
    
    #위에서 구한 features에 적절한 가중치를 주어 값을 반환한다.
    return features['noWay']*1+features['canCatchN']*100+features['goToHome']*(-76)+features['havingFood']*190+features['canCatch']*1+features['distanceToFood']*(-139.5)+features['distanceToGhost']*80+features['numOfGhost']*(-15)+features['nextScore']*8000+features['successorScore']*(-3200)+features['leftCapsules']*(-3000)+features['distanceToCapsule']*(-218.5)

#일부 상황에서는 공격, 일부 상황에서는 수비를 담당하는 agent이다.
class defense(PlanningCaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    #이 클래스는 CaptureAgent를 상속했으므로, CaptureAgent의 초기화함수를 호출해준다.
    CaptureAgent.registerInitialState(self, gameState)
    #이 클래스는 PlanningCaptureAgent를 상속했으므로, PlanningCaptureAgent의 초기화함수를 호출해준다.
    PlanningCaptureAgent.registerInitialState(self,gameState)
    #처음 출발 위치를 start에 저장
    self.start = gameState.getAgentPosition(self.index)

  def chooseAction(self, gameState):
    """
    Picks among actions randomly.
    """    
    #현재 탐색 중인 agent가 취할수 있는 행동을 actions에 저장 
    actions = gameState.getLegalActions(self.index)
    #현재 남은 음식의 개수를 foodLeft에 저장
    foodLeft = len(self.getFood(gameState).asList())

    #bestAct를 선언하고 0으로 초기화
    bestAct = 0
    #만약 음식이 2개 이하로 남았다면
    if foodLeft<=2:
      #출발점과의 최소 거리를 bestDist라고 선언하고 초기값을 9999로 지정
      bestDist = 9999
      #가능한 행동들 사이에서 출발점과 가장 가까운 곳으로 가는 행동을 찾는다.
      for action in actions:
        #action을 취했을 때 도달하는 상태를 successor에 저장
        successor = self.getSuccessor(gameState, action)
        #successor의 위치를 pos2에 저장
        pos2 = successor.getAgentPosition(self.index)
        #출발점과 pos2사이의 거리를 dist에 저장
        dist = self.getMazeDistance(self.start,pos2)
        #만약 dist가 bestDist보다 작다면 (최소값을 구하는 과정)
        if dist < bestDist:
          #그때의 action을 bestAct에 저장한다.
          bestAct = action
          #그때의 거리를 bestDist라고 한다.
          bestDist = dist
      #최종적으로 선택된 bestAct를 반환한다.
      return bestAct
    #현재 남은 음식의 개수가 2보다 클 경우
    else:
      #getAction에서 받은 행동을 bestAction에 저장
      bestAction = self.getAction(gameState)
      #bestAction을 반환한다.
      return bestAction


  def getFeatures(self, gameState):
    #적들의 상태를 enemies에 저장
    enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
    #적들 중 현재 우리 영역에 있는 침입자들의 상태를 invader에 저장
    invaders = [a for a in enemies if a.isPacman and (a.getPosition() != None)]

    #만약 침입자가 0명이면
    if len(invaders)==0:
      #Counter로 features를 선언한다.
      features = util.Counter()
      
      #현재 탐색 대상인 agent(나)의 위치를 pos에 저장한다.
      pos = gameState.getAgentPosition(self.index)
      #적들 중 현재 상대의 영역에 있으면서 방어를 하는 ghost들의 상태를 defenders에 저장한다.
      defenders = [a for a in enemies if (a.isPacman==False) and (a.getPosition() != None)]

      #먹어야 할 음식을 list의 형태로 foodList에 저장한다.
      foodList = self.getFood(gameState).asList()
      #먹어야 할 capsule에 대한 정보를 capsuleList에 저장한다.
      capsuleList = self.getCapsules(gameState)
      #벽에 대한 정보를 wall에 저장한다.
      wall = gameState.getWalls()

      #numOfGhost features에 defenders의 길이를 저장한다.
      features['numOfGhost']=len(defenders)
      #nextScore features에 현재 점수를 저장한다.
      features['nextScore']=self.getScore(gameState)
      #successorScore features에 foodList의 길이를 저장한다.
      features['successorScore'] = len(foodList)
      #leftCapsules features에 capsuleList의 길이를 저장한다.
      features['leftCapsules'] = len(capsuleList)
       #canCatchN features에 0을 저장한다.
      features['canCatchN'] = 0

      #아직 pacman이 아닐때
      if gameState.getAgentState(self.index).isPacman == False:
        #적들과의 최소거리를 구한다.
        for enemy in enemies:
          dist = self.getMazeDistance(pos, enemy.getPosition())
          #만약 적과의 거리가 1보다 작거나 같다면(잡을 확률이 높다)
          if dist<=1:
            #canCatchN features에 1을 저장한다.
            features['canCatchN'] = 1

      #음식과의 최소 거리 구하기
      if len(foodList) > 0: # This should always be True,  but better safe than sorry
        minFDist = min([self.getMazeDistance(pos, food) for food in foodList])
        #음식과의 최소거리를 distanceToFood features에 저장한다.
        features['distanceToFood'] = minFDist

      #ghost와의 최소거리 구하기
      #minGDist를 선언하고 1000으로 초기화한다.
      minGDist = 1000
      #가장 가까운 ghost의 index를 minIndex라고 선언하고 0을 저장하였다.
      minIndex = 0
      #만약 defender가 있을 경우
      if len(defenders)>0:
        #가장 가까운 ghost와의 거리와 그 ghost의 index를 구한다.
        for i,defender in enumerate(defenders):
          #dist는 현재 탐색중인 agent(나)와 defender사이의 거리이다.
          dist = self.getMazeDistance(pos, defender.getPosition())
          #만약 minGDist보다 dist가 더 작을 경우
          if minGDist>dist:
            #minGDist를 dist라고 하자.
            minGDist = dist
            #minIndex를 i라고 하자.
            minIndex = i
      #distanceToGhost features에 minGDist를 저장한다.
      features['distanceToGhost'] = minGDist
      
      #적과의 거리가 2이하일때, 죽을 위기 일때
      if minGDist<=2:
        #만약 탐색중인 agent(나)가 pacman이 아니라면 상대를 잡을 수 있는 상태이다.
        if gameState.getAgentState(self.index).isPacman == False:
            #canCatch features에 5000을 저장한다.
            features['canCatch'] =5000
            #distanceToGhost featuresdp 10*minGDist를 저장하여 거리가 줄어들때 더 많은 점수가 증가하도록 하였다.
            features['distanceToGhost'] = 10*minGDist
        #탐색중인 agent(나)가 pacman이라면
        else:
          #만약 가장 가까운 defender가 scared상태이고, scaredTimer가 4보다 많이 남았다면
          if defenders[minIndex].scaredTimer>4:
            #잡을 수 있으므로 canCatch features에 5000을 저장한다.
            features['canCatch'] =5000
            #distanceToGhost features에 minGDist를 저장한다.
            features['distanceToGhost'] = minGDist
            #distanceToFood features에 2*minFDist를 저장하여 음식과의 거리에 가중치를 더 주었다.
            #ghost와의 거리보다 음식을 먹는 것에 집중하기 위함이다.
            features['distanceToFood'] = 2*minFDist
          #만약 scaredTime이 4보다 작고 0보다 클 경우
          elif defenders[minIndex].scaredTimer>0:
            #이때는 잡아야하므로, 거리가 가까워짐에 비례하여 canCatch features가 커지도록 하였다.
            features['canCatch'] = 5000*(1-minGDist)
          #만약 상대가 scared상태가 아니라면
          else:
            #도망쳐야하므로 canCatch features에 -5000을 저장한다.
            features['canCatch'] =-5000
            #ghost와의 거리가 작으면 좋지 않으므로, -7을 곱해주어 애초에 minGDist가 1보다 작거나 같은 상황을 피하도록 하였다.
            features['distanceToGhost'] = -7*minGDist
      
      #만약 남은 음식의 개수가 2개보다 작거나 같다면
      if len(foodList)<=2:
        #음식을 더이상 먹지 않을 것이므로 가장 가까운 음식과의 거리를 0으로 한다.
        features['distanceToFood'] = 0

      #powerCapsule
      #만약 powerCapsule의 개수가 0개보다 크다면
      if len(capsuleList)>0:
        #powerCapsule와의 최소 거리를 minCdist에 저장한다.
        minCDist = min([self.getMazeDistance(pos,capsule) for capsule in capsuleList])
        #distanceToCapsule features에 minCDist를 저장한다.
        features['distanceToCapsule'] = minCDist

      #탐색중인 agent(나)의 주변에 있는 벽의 개수를 wallNum이라고 하자.
      wallNum = 0
      #탐색해야하는 위치가 map끝쪽이면 오류가 발생하므로 try-except문을 사용하였다.
      try:
        #만약 탐색중인 agent(나)가 pacman이라면
        if gameState.getAgentState(self.index).isPacman:  
          #내 주변의 벽을 검사하기 위해 배열 ar을 선언하였다.
          ar = [(-0.5,0),(0.5,0),(0,-0.5),(0,0.5)]
          for i in ar:
              #내 주변에 벽이 있다면
              if gameState.hasWall(pos[0]+i[0],pos[1]+i[1]):
                #wallNum을 1증가시킨다.
                wallNum = wallNum+1
      except:
        i=0
      
      #만약 주변에 벽이 3개가 있다면
      if wallNum == 3:
        #noWay features에 -1000을 저장한다.
        features['noWay'] = -1000
        #이때 내 위치에 음식이 없다면
        if self.getFood(gameState)[pos[0]][pos[1]]==False:
          #가면 안되므로 noWay features에 -1000000을 저장한다.
          features['noWay'] = -1000000

      #만약 탐색중인 agent(나)가 pacman이라면
      if gameState.getAgentState(self.index).isPacman==True:
        #가지고 있는 음식의 개수를 havingFood에 저장한다.
        havingFood = gameState.getAgentState(self.index).numCarrying
        #가지고 있는 음식의 개수를 havingFood에 저장한다.
        minHDist = abs(pos[0]-(wall.width//2)) 
        #만약 minHDist가 0이 아니라면
        if minHDist!=0:
          #having Food features에 havingFood/minHdist를 저장한다.
          #이때 가지고 있는 음식의 개수가 늘어나면 좋지만, 경계선과의 거리가 멀어지면 좋지 않으므로 이를 반영하였다.
          features['havingFood'] = havingFood/minHDist
        #만약 minHDist가 0이면
        else:
          #havingFood features에 havingFood를 저장하였다.
          features['havingFood'] = havingFood
      
         #만약 가지고있는 음식의 개수가 2보다 크거나 같다면
        if havingFood>=2:
          #goToHome features에 minHDist를 저장한다.
          features['goToHome'] = minHDist
          
      return features['noWay']*1+features['canCatchN']*100+features['goToHome']*(-76)+features['havingFood']*190+features['canCatch']*1+features['distanceToFood']*(-139.5)+features['distanceToGhost']*80+features['numOfGhost']*(-15)+features['nextScore']*8000+features['successorScore']*(-3200)+features['leftCapsules']*(-3000)+features['distanceToCapsule']*(-218.5)


    #침입자가 있을때
    else:
      #Counter로 features를 선언한다.
      features = util.Counter()
      #현재 탐색 대상인 agent(나)의 위치를 pos에 저장한다.
      pos = gameState.getAgentPosition(self.index)
      #현재 탐색 대상인 agnet(나)의 상태를 MyState에 저장한다.
      myState = gameState.getAgentState(self.index)
      #막아야 할 음식을 list의 형태로 foodList에 저장한다.
      foodList = self.getFoodYouAreDefending(gameState).asList()
      #막아야 할 capsule에 대한 정보를 capsuleList에 저장한다.
      capsuleList = self.getCapsulesYouAreDefending(gameState)

      #onDefense features에 1을 저장한다.(현재 수비중)
      features['onDefense'] = 1
      #만약 탐색중인 agent(나)가 pacman이면 onDefense features에 0을 저장한다.
      if myState.isPacman:
        features['onDefense'] = 0
      
      #numOfInvadors features에 invaders의 길이를 저장한다.
      features['numOfInvadors']=len(invaders)
      #leftCapsules features에 capsuleList의 길이를 저장한다.
      features['leftCapsules'] = len(capsuleList)

      #음식과의 최소 거리 구하기
      if len(foodList) > 0: # This should always be True,  but better safe than sorry
        minFDist = min([self.getMazeDistance(pos, food) for food in foodList])
        #음식과의 최소거리를 distanceToFood features에 저장한다.
        features['distanceToFood'] = minFDist

      #invader와의 최소거리 구하기
      #minIDist를 선언하고 1000으로 초기화한다.
      minIDist = 10000
      #만약 invader가 있을 경우
      if len(invaders)>0:
        #가장 가까운 invader과의 거리를 구한다.
        for invader in invaders:
          #dist는 현재 탐색중인 agent(나)와 invader사이의 거리이다.
          dist = self.getMazeDistance(pos, invader.getPosition())
          #만약 minGDist보다 dist가 더 작을 경우
          if minIDist>dist:
            #minGDist를 dist라고 하자
            minIDist = dist
        #distanceToInvador features에 minIDist를 저장한다.
        features['distanceToInvador'] = minIDist
        #invader과의 거리가 1이하일때, 잡을 가능성이 높을때
        if minIDist<=1:
          #잡을 확률이 높으므로 nextScore features도 1000으로 저장한다.
          features['nextScore'] = 1000
          #만약 my state가 scared이면
          if myState.scaredTimer>0:
            #이때는 잡히지 말아야하므로, 거리가 가까워에 비례하여 canCaught features가 많은 양 감소하게 하였다.
            features['canCaught'] = -1000*(3-minIDist)
          #my state가 scared가 아니면
          else:
            #이때는 잡아야하므로, 거리가 가까워에 비례하여 canCaught features가 많은 양 증가하게 하였다.
            features['canCaught'] = 1000*(3-minIDist)
              
      #invader이 없으면
      else:
        #enemy와의 최소 거리를 구한다.
        for enemy in enemies:
          #dist는 탐색중인 agent(나)와 enemy사이의 거리이다.
          dist = self.getMazeDistance(pos, enemy.getPosition())
          #만약 minIDist가 dist보다 크다면
          if minIDist>dist:
            #minIDist에 dist를 저장한다.
            minIDist = dist
        #distanceToInvador features에 minIDist를 저장한다.
        features['distanceToInvador'] = minIDist
      
      #powerCapsule
      #만약 powerCapsule의 개수가 0개보다 크다면
      if len(capsuleList)>0:
          #powerCapsule와의 최소 거리를 minCdist에 저장한다.
          minCDist = min([self.getMazeDistance(pos,capsule) for capsule in capsuleList])
          #distanceToCapsule features에 minCDist를 저장한다.
          features['distanceToCapsule'] = minCDist

      #적이 근처에 있을 경우 
      try:
        #이전 상태가 없으면 오류가 발생하므로 try구문을 사용하였다.
        #이전 상태를 previous에 저장하였다.
        previous = self.getPreviousObservation()
        #이전 상태에서의 적을 pre_ene에 저장하였다.
        pre_ene = [previous.getAgentState(i) for i in self.getOpponents(gameState)]
        #이전 상태에서의 invader를 pre_inv에 저장하였다.
        pre_inv = [a for a in pre_ene if a.isPacman and (a.getPosition() != None)]
        #만약 이전 상태에서 침입자의 수가 현재 상태의 침입자 수보다 많을 경우
        if len(pre_inv)>len(invaders):
          #catch P features에 1000 저장한다.
          features['catchP'] = 1000
      except:
        i=0
      

      #위에서 구한 features에 적절한 가중치를 주어 값을 반환한다
      return features['catchP']+features['onDefense']*1000+features['canCaught']*100+features['distanceToFood']*(-150) +features['distanceToInvador']*(-500)+features['numOfInvadors']*(-5000)+features['nextScore']*500+features['leftCapsules']*2000+features['distanceToCapsule']*(-200)
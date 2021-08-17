# Artificial-Intellignece---2021-1st-semester-Korea-University
--------
## 프로젝트 개요
> 각 프로젝트마다 주어진 상황이 있다. 각 상황에 맞게 최고 점수를 얻게끔 나의 Agent를 설계해야한다. 
> 
> 게임 규칙은 아래와 같다.
> 1. Pacman이 상대 agent에게 먹히면 출발점으로 돌아온다.
> 2. Pacman이 작은 dot을 먹을때마다 10점이 증가하며 큰 dot을 먹으면 일정시간동안 상대 agent를 잡아먹을 수 있게 된다.
> 3. dot을 다 먹어 더이상 map에 dot이 없게되면 승리한다. 또는 시간이 모두 흘렀을때 점수가 0보다 크다면 승리한다.
> 
----
## Final Project1
### 1. 프로젝트 설명
> ![image](https://user-images.githubusercontent.com/65549245/129654733-fb9af1b7-b95f-4161-957d-febd8a64514b.png)
> (출처 : cs188)
> 
> 4개의 agent를 설계하여 score가 0이되기 전에 모든 dot을 먹으면 승리한다.
> score는 시간이 흐를수록 감소하고, dot을 먹을때마다 증가한다.
> 이때 dot을 빨리 많이 먹을 수록 높은 점수로 게임에서 승리할 수 있다.
> 
### 2. MyAgents 설계
> ClosestDotAgent를 참고하여 MyAgent를 작성하였다. ClosestDotAgent는 매 순간 가장 가까운 목적지(Food)로 가는 Agent이다.
> MyAgent에서는 각 agent가 어떠한 목적지(Food)로 향하는지를 저장한 GoingList, 목적지까지 가기 위해 해야 할 action들을 저장한 actionList, actionList의 길이를 저장한 actionLength를 이용하여 탐색을 진행하였다. 
> 
> 1.agent의 actionList가 비어있을 경우 경로 탐색을 시작한다. 목적지를 찾기 전까지의 탐색 방식은 BFS와 유사하다.
> 
> 2.목적지를 찾은 다음 GoingList에 현재 찾은 목적지와 같은 목적지가 있는지 없는지 검사한다.
> 
> 2-1. 만약 같은 목적지가 없다면 GoingList[self.index]에 해당 목적지의 위치를, actionList[self.index]에는 결과로 나온 action들의 집합을, actionLength[self.index]에는 actionList의 길이를 저장한다.
> 
> 2-2. 만약 같은 목적지(G)가 GoingList에 이미 있다면 agent(A)가 찾은 경로가 현재 G로 가고 있는 다른 agent(B)의 경로보다 짧은지 확인해야 한다.
> 
> 2-2-1. 만약 더 짧다면 B의 GoingList를 (-1,-1)로, actionList를 []로, actionLength를 0으로 초기화하고 A의 GoingList에 목적지를, 목적지까지
의 경로를 actionList에, 그 경로의 길이를 actionLength에 저장해준다.

> 2-2-2. 만약 A의 경로가 B의 경로보다 더 길다면, 현재 방문한 목적지(Food)의 위치를 visitedPosition에 추가하고 continue를 사용해 탐색 재개하여 다음 목적지(Food)를 찾는다. 
> 
### 3. 성과
> 과제 통과 기준은 500점이었으며 수강생들끼리 결과를 비교하여 상위권에 있는 사람들에게 추가 점수를 주는 구조였다.
> 
> 795점을 획득하였으며, 상위 2번째 그룹에 포함되어 추가 점수 2점을 받았다.
> 
--------

## Final Project2
### 1. 프로젝트 설명
> ![image](https://user-images.githubusercontent.com/65549245/129656063-981ce110-f85b-4504-9f8c-43caab2256a4.png)
> (출처 : cs188)
> 
> Final project2에서는 상대방과 겨루어 승자를 가린다.게임 상에서 map은 내 진영과 상대 진영 두 부분으로나누어져 있다. 각 팀은 두 개의 agent를 가지고 있다.
> 
> 우리 팀 agent가 상대 진영으로 넘어가면 pacman으로 바뀐다 (이를 공격자라고 부르겠다). 공격자는 상대진영에 있는 ghost를 피해 food를 먹고 내 진영으로 다시 가져와야 한다. 이때 가져온 food의 개수만큼 score는 증가한다. 만약 돌아오기 전에 ghost에게 잡히면 공격자는 자기 진영의 출발점으로 돌아오게 되고 가지고 있었던 food들은 ghost에게 먹힌 자리에 남겨진다. 상대 진영에 food 두 개를 남기고 먼저 18개를 내 진영으로 가져오거나 시간이 다 되었을 때 점수가 높으면 승리한다.
> 
### 2. MyAgents 설계
> + baseline1 
>   + 공격자와 수비자를 나누어 설계
>     + Alpha-Beta Pruning을 이용한 Minimax Search를 사용하여 다음에 할 행동을 정하였다.
>     
> + baseline2
>   + 공격자와 수비자를 나누어 설계
>     + Expectimax Search를 사용하여 다음에 할 행동을 정하였다
>
> + baseline3
>   + 공격자와 수비자를 따로 나누지 않고 두 가지 기능을 함께하는 agent를 설계(all rounder agent)
>     + Alpha-Beta Pruning을 이용한 Minimax Search를 사용하여 다음에 할 행동을 정하였다.


### 3. 최종적으로 선택한 baseline
> 3개의 baseline중 가장 승률이 좋은 your baseline3를 best로 설정하였다.
>
> all rounder agent는 상황에 맞게 행동을 선택하기 때문에 다양한 state에 대해 유연하게 대처할 수 있다. 경쟁에서 이겨야 하는 상황에서 이 agent는 좋은 성능을 보여 줄것 이다. 따라서 your baseline3를 best로 정하였다.

### 4. 성과
> baseline3는 baseline1, baseline2, baseline3, baseline(기본적으로 제공되는 상대 기준점)
> 
> 
--------
## 총평
> A+를 받음

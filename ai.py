from enum import EnumMeta
import math
from QuoridorBoard import QuoridorBoard
from Coordinate import Coordinate
from QuoridorMove import QuoridorMove
from QuoridorMove import QuoridorMoveType
LEN_GRID = 9

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        return self.position == other.position

class AnirudhConor():
    
    def __init__(self, game):
        self.game = game

    def astar(self, board,start,player):
        
        startNode = Node(None, start)
        goalNodes = []
        if(player==0):
            for i in range(9):
                goalNodes.append(Node(None,(i,8)))
        if(player==1):
            for i in range(9):
                goalNodes.append(Node(None, (i,0)))
        open = [startNode]
        closed = []

        while len(open) > 0:
            
            curNode = open[0]
            curIndex = 0
            for index, node in enumerate(open):
                if node.f < curNode.f:
                    curNode = node
                    curIndex = index
            open.pop(curIndex)
            closed.append(curNode)

            if curNode in goalNodes:
                path = []
                cur = curNode
                while cur is not None:
                    path.append(cur.position)
                    cur = cur.parent
                return path[::-1]

            children = []
            possible_moves=[(0, -1), (0, 1), (-1, 0), (1, 0)]
            newMoves=[]
            for move in possible_moves:
                newMoves = board.possible_jumps(Coordinate(curNode.position[0], curNode.position[1]), Coordinate(curNode.position[0] + move[0], curNode.position[1] + move[1]))
            if(len(newMoves)>0):   
                if curNode.position[0]==newMoves[0].x:
                    if curNode.position[1]>newMoves[0].y:
                        possible_moves.remove((0,-1))
                        possible_moves.append((0,-2))
                    elif curNode.position[1]<newMoves[0].y:
                        possible_moves.remove((0,1))
                        possible_moves.append((0,2))
                if curNode.position[1]==newMoves[0].y:
                    if curNode.position[0]>newMoves[0].x:
                        possible_moves.remove((-1,0))
                        possible_moves.append((-2,0))
                    elif curNode.position[0]<newMoves[0].x:
                        possible_moves.remove((1,0))
                        possible_moves.append((2,0))
            
            for newPos in possible_moves:
                nodePos = (curNode.position[0] + newPos[0], curNode.position[1] + newPos[1])
                if (nodePos[0] > LEN_GRID - 1) or (nodePos[0] < 0) or (nodePos[1] > LEN_GRID - 1) or (nodePos[1] < 0):
                    continue
                if not board.check_fences(Coordinate(curNode.position[0], curNode.position[1]), Coordinate(nodePos[0], nodePos[1])):
                    continue
                newNode = Node(curNode, nodePos)
                if newNode not in closed:
                    children.append(newNode)

            for child in children:
                if child in closed:
                    continue
                child.g = curNode.g + 1
                heuristics = []
                for goalNode in goalNodes:
                    heuristics.append(math.sqrt((child.position[0] - goalNode.position[0]) ** 2) + math.sqrt((child.position[1] - goalNode.position[1]) ** 2))
                child.h = min(heuristics)
                child.f = child.g + child.h
                inList = False
                for openNode in open:
                    if child == openNode and child.g > openNode.g: # make sure this is comparing correctly
                        inList = True
                        break
                if not inList:
                    open.append(child)


    def getOurPath(self,board,start,player):
        path=self.astar(board,start,player)
        return path
        
    def getTheirPath(self,board,enemy_player):
        path=self.astar(board,(board.pawns[enemy_player].x,board.pawns[enemy_player].y),enemy_player)
        return path

    def getBestFence(self,board,player,enemy_player):
        fences=board.get_legal_fences(player)
        bestFence=0
        longest_path=0
        for fence in fences:
            move= QuoridorMove()
            next_board=self.game.getNextState(board, player, fence)
            potential_path=self.getTheirPath(next_board[0],enemy_player)

            if longest_path==0 or longest_path<len(potential_path):
                longest_path=len(potential_path)
                bestFence=fences.index(fence)
        
        return fences[bestFence], longest_path
    
    def getBestMove(self, board,player,enemy_player,valid_moves):
        #begin by grabbing board value
        #then grab a* values for our pawn
        win_path=self.getOurPath(board,(board.pawns[player].x,board.pawns[player].y),player) # fix indexing
        #grab their a* value
        lose_path=self.getTheirPath(board,enemy_player)
        
        if board.fences[player] > 0:
            best_fence=self.getBestFence(board,player,enemy_player)
        
        move_turn=True
        print(win_path)
        print("\n")
        print(lose_path)
        
        # move.coord=Coordinate(win_path[0],win_path[1])
        # move.type = QuoridorMoveType.MOVE
        # move.player = player
        for move in valid_moves:
                if win_path[1][0]==move.coord.x and win_path[1][1]==move.coord.y and move.type==QuoridorMoveType.MOVE:
                    move_value=self.evaluate(self.game.getNextState(board,player,move)[0],player,enemy_player)
        if board.fences[player] > 0:
            fence_value=self.evaluate(self.game.getNextState(board,player,best_fence[0])[0],player,enemy_player)
        if board.fences[player] > 0:
            if fence_value>move_value:
                move_turn=False
                return move_value,best_fence[0], move_turn
            else:
                if len(win_path)<1:
                    return move_value,win_path[0],move_turn
                return move_value,win_path[1],move_turn
        
        
        if len(win_path)<1:
            return move_value,win_path[0],move_turn
        return move_value,win_path[1],move_turn

        
    def play(self, board, valid_moves):
        enemy_player=-1
        if board.current_player==1:
            enemy_player=0
        else:
            enemy_player=1
        
        
        best=self.getBestMove(board,board.current_player,enemy_player,valid_moves)
                
        if best[2]==False:
            return best[1]
        else:
            for move in valid_moves:
                if best[1][0]==move.coord.x and best[1][1]==move.coord.y and move.type==QuoridorMoveType.MOVE:
                    return move
    
    def evaluate(self,board, ours, theirs):
        our_path=self.getOurPath(board,(board.pawns[ours].x,board.pawns[ours].x),ours)
        their_path=self.getTheirPath(board,ours)
        
        our_dist=len(our_path)
        their_dist=len(their_path)
         
        our_fences=board.fences[ours]
        their_fences=board.fences[theirs]
        fence_agro=0
        for fence in board.vertical_fences:
            if ours ==0:
                if fence.first.y>4:
                    fence_agro+1
            elif ours ==0:
                if fence.first.y<4:
                    fence_agro+1
        for fence in board.horizontal_fences:
            if ours ==0:
                if fence.first.y>4:
                    fence_agro+1
            elif ours ==0:
                if fence.first.y<4:
                    fence_agro+1
                    
        return (their_dist-our_dist)+((our_fences + 1)/(their_fences + 1))+fence_agro

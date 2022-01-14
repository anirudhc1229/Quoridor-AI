from Coordinate import Coordinate
from enum import Enum

class QuoridorMoveType(Enum):
    MOVE = 0
    FENCE = 1

class QuoridorMove(object):
    """
    One move in Quoridor
    """

    def move_pawn(new_coord, player):
        move = QuoridorMove()
        move.type = QuoridorMoveType.MOVE
        move.coord = new_coord
        move.player = player
        return move

    def add_fence(fence, player):
        move = QuoridorMove()
        move.type = QuoridorMoveType.FENCE
        move.coord = fence.first
        move.is_horizontal = fence.is_horizontal
        move.player = player
        return move

    def execute(self, board):
        if self.type == QuoridorMoveType.MOVE:
            board.move_pawn(self.player, self.coord)
        elif self.type == QuoridorMoveType.FENCE:
            board.add_fence(self.player, self.coord, self.is_horizontal)
        else:
            raise Exception("Impossible move!")




from collections import namedtuple
import numpy as np
from Coordinate import Coordinate
from QuoridorMove import QuoridorMove

class Fence:
    def __init__(self, first, is_horizontal):
        self.first = first
        self.is_horizontal = is_horizontal

    # See if you can move from current to final without hitting this wall
    def test_move(self, current, final):
        if self.is_horizontal:
            if (current.y == self.first.y - 1 and final.y == self.first.y) or (final.y == self.first.y - 1 and current.y == self.first.y):
                if current.x == self.first.x or current.x == self.first.x + 1:
                    return False
                else:
                    return True
            else:
                return True
        else:
            if (current.x == self.first.x - 1 and final.x == self.first.x) or (final.x == self.first.x - 1 and current.x == self.first.x):
                if current.y == self.first.y or current.y == self.first.y + 1:
                    return False
                else:
                    return True
            else:
                return True

    # Find which moves are blocked by this fence
    def forbidden_moves(self):
        if self.is_horizontal:
            return [(Coordinate(self.first.x, self.first.y), Coordinate(self.first.x, self.first.y - 1)),
                    (Coordinate(self.first.x, self.first.y - 1), Coordinate(self.first.x, self.first.y)),
                    (Coordinate(self.first.x + 1, self.first.y), Coordinate(self.first.x + 1, self.first.y - 1)),
                    (Coordinate(self.first.x + 1, self.first.y - 1), Coordinate(self.first.x + 1, self.first.y))]
        else:
            return [(Coordinate(self.first.x, self.first.y), Coordinate(self.first.x - 1, self.first.y)),
                    (Coordinate(self.first.x - 1, self.first.y), Coordinate(self.first.x, self.first.y)),
                    (Coordinate(self.first.x, self.first.y + 1), Coordinate(self.first.x - 1, self.first.y + 1)),
                    (Coordinate(self.first.x - 1, self.first.y + 1), Coordinate(self.first.x, self.first.y + 1))]

    # Check for conflicts between two fences
    def check_conflict(self, other):
        if self.is_horizontal == other.is_horizontal:
            return self.check_overlap(other)
        else:
            return self.check_crossing(other)

    # Check for overlaps between two fences, given that the two have the same orientation
    def check_overlap(self, other):
        if self.is_horizontal:
            return self.first.y == other.first.y and abs(self.first.x - other.first.x) < 2
        else:
            return self.first.x == other.first.x and abs(self.first.y - other.first.y) < 2

    # Check for crossings between two fences, given that the two have opposite orientation
    def check_crossing(self, other):
        if self.is_horizontal:
            return self.first.x + 1 == other.first.x and other.first.y + 1 == self.first.y
        else:
            return other.first.x + 1 == self.first.x and self.first.y + 1 == other.first.y

class QuoridorBoard:
    """
    Quoridor Board.
    """

    def __init__(self, n_players):
        "Set up initial board configuration."

        self.horizontal_fences = []
        self.vertical_fences = []
       # self.forbidden_moves = {}
        self.check_possible = True

        if n_players == 2:
            self.pawns = [Coordinate(4, 0), Coordinate(4, 8)]
            self.fences = [10, 10]
        elif n_players == 4:
            self.pawns = [Coordinate(4, 0), Coordinate(0, 4), Coordinate(4, 8), Coordinate(8, 4)]
            self.fences = [5, 5, 5, 5]
        else:
            raise Exception("Illegal number of players")

        self.current_player = 0

    # Move the pawn
    def move_pawn(self, player, new_coord):
        if self.is_legal_move(player, new_coord):
            self.pawns[player] = new_coord
        else:
            raise Exception("Illegal move!")

    # Add a fence
    def add_fence(self, player, coord1, is_horizontal):
        if self.fences[player] == 0:
            raise Exception("No fences remain!")
        new_fence = Fence(coord1, is_horizontal)
        for fence in self.all_fences():
            if fence.check_conflict(new_fence):
                raise Exception("Fence in illegal location!")
        if new_fence.is_horizontal:
            self.horizontal_fences.append(new_fence)
        else:
            self.vertical_fences.append(new_fence)

        #for coord_pair in new_fence.forbidden_moves():
        #    if coord_pair[0] not in self.forbidden_moves:
        #        self.forbidden_moves[coord_pair[0]] = []
        #    self.forbidden_moves[coord_pair[0]].append(coord_pair[1])

        self.fences[player] -= 1

    # Check if this move is allowed
    def is_legal_move(self, player, new_coord):
        return new_coord in self.get_legal_move_positions_for_player(player)

    # Check if you can move from current to new_coord without going through any fence in the fences collection
    def test_fences(self, fences, current, new_coord):
        for fence in fences:
            if not fence.test_move(current, new_coord):
                return False
        return True

    # Check if you can move from current to new_coord without going through any fences
    def check_fences(self, current, new_coord):
        return (current.x == new_coord.x and self.test_fences(self.horizontal_fences, current, new_coord)) or (current.y == new_coord.y and self.test_fences(self.vertical_fences, current, new_coord))
        #if current not in self.forbidden_moves:
        #    return True
        #else:
        #    return new_coord not in self.forbidden_moves[current]

    # Get all possible positions you can jump to if you are on current and another pawn is on move
    def possible_jumps(self, current, move):
        if not self.is_occupied(move):
            return []
        # Choose target jump
        if current.x == move.x:
            if current.y > move.y:
                target = Coordinate(current.x, current.y - 2)
            else:
                target = Coordinate(current.x, current.y + 2)
        else:
            if current.x > move.x:
                target = Coordinate(current.x - 2, current.y)
            else:
                target = Coordinate(current.x + 2, current.y)

        if not target.is_legal():
            return []

        if self.check_fences(move, target) and not self.is_occupied(target):
            return [target]
        else:
            # Get new targets
            if current.x == move.x:
                new_targets = [Coordinate(current.x - 1, move.y), Coordinate(current.x + 1, move.y)]
            else:
                new_targets = [Coordinate(move.x, current.y - 1), Coordinate(move.x, current.y + 1)]

            final_moves = []
            for new_target in new_targets:
                if self.check_fences(move, new_target) and not self.is_occupied(new_target):
                    final_moves.append(new_target)
            return final_moves


    # Gets all legal moves for a given player's pawn - pawn moves only
    def get_legal_move_positions_for_player(self, player):
        return self.get_legal_move_positions(self.pawns[player])

    # These are moves for the pawn moves only
    def get_legal_move_positions(self, current):
        moves = []
        potential_moves = [Coordinate(current.x - 1, current.y), Coordinate(current.x, current.y - 1), Coordinate(current.x + 1, current.y), Coordinate(current.x, current.y + 1)]
        for move in potential_moves:
            # Make sure it's legal
            if not move.is_legal():
                continue
            # Check for fences
            if self.check_fences(current, move):
                # Check for occupied spaces
                if self.is_occupied(move):
                    for jump in self.possible_jumps(current, move):
                        moves.append(jump)
                else:
                    moves.append(move)

        return moves

    def all_fences(self):
        return self.horizontal_fences + self.vertical_fences

    # These are possible fences
    def get_legal_fences(self, player):
        if (self.fences[player] == 0):
            return []
        fences = []
        # Horizontal 
        for ix in range(0, 8):
            for iy in range(1, 9):
                potential_fence = Fence(Coordinate(ix, iy), True)
                found_conflict = False
                for fence in self.all_fences():
                    if fence.check_conflict(potential_fence):
                        found_conflict = True
                        break
                if found_conflict:
                    continue
                if self.check_possible:
                    if not self.check_if_possible(potential_fence):
                        continue
                fences.append(QuoridorMove.add_fence(potential_fence, self.current_player))
        # Vertical
        for ix in range(1, 9):
            for iy in range(0, 8):
                potential_fence = Fence(Coordinate(ix, iy), False)
                found_conflict = False
                for fence in self.all_fences():
                    if fence.check_conflict(potential_fence):
                        found_conflict = True
                        break
                if found_conflict:
                    continue
                if self.check_possible:
                    if not self.check_if_possible(potential_fence):
                        continue
                fences.append(QuoridorMove.add_fence(potential_fence, self.current_player))
        return fences

    # Check to make sure it is still possible to get across the board
    def check_if_possible(self, new_fence):
        for i_player in range(len(self.pawns)):
            if not self.check_if_possible_single_player(i_player, new_fence):
                return False
        return True

    # Check to make sure it is still possible to get across the board for a single player
    def check_if_possible_single_player(self, player, new_fence):
        win_condition = self.get_target(player)

        # Provisionally add the new fence
        if new_fence.is_horizontal:
            self.horizontal_fences.append(new_fence)
        else:
            self.vertical_fences.append(new_fence)

        # Dijkstra's algorithm, modified
        already_tested = {}
        # Start with current pawn location
        to_be_tested = [self.pawns[player]]
        while to_be_tested:
            new_to_be_tested = []
            for point in to_be_tested:
                for new_point in self.get_legal_move_positions(point):
                    if win_condition(new_point):
                        # Remove the added fence
                        if new_fence.is_horizontal:
                            self.horizontal_fences.pop(len(self.horizontal_fences) - 1)
                        else:
                            self.vertical_fences.pop(len(self.vertical_fences) - 1)
                        return True
                    if not new_point in already_tested:
                        already_tested[new_point] = 0
                        new_to_be_tested.append(new_point)
            to_be_tested = new_to_be_tested

        # This means no win condition was found
        # So remove the added fence
        if new_fence.is_horizontal:
            self.horizontal_fences.pop(len(self.horizontal_fences) - 1)
        else:
            self.vertical_fences.pop(len(self.vertical_fences) - 1)
        return False

    # Return a lambda function which determines if a coordinate satisfied the win condition for a particular player
    def get_target(self, player):
        if player == 0:
            return lambda a : a.y == 8
        if player == 1:
            if len(self.pawns) == 2:
                return lambda a : a.y == 0
            elif len(self.pawns) == 4:
                return lambda a : a.x == 8
        if player == 2:
            return lambda a : a.y == 0
        if player == 3:
            return lambda a : a.x == 0

        raise Exception("Illegal player number entered")

    # Check if a square is occupied by another pawn
    def is_occupied(self, coord):
        for player in self.pawns:
            if coord == player:
                return True
        return False

    # Gets a list of all possible moves
    def get_valid_moves(self):
        return self.get_legal_moves_for_player(self.current_player) + self.get_legal_fences(self.current_player)

    def get_legal_moves_for_player(self, player):
        legal_moves = []
        for move in self.get_legal_move_positions_for_player(player):
            legal_moves.append(QuoridorMove.move_pawn(move, player))
        return legal_moves

    # Switch to next player
    def next_player(self):
        if len(self.pawns) == 2:
            if self.current_player == 1:
                self.current_player = 0
            else:
                self.current_player = 1
        elif len(self.pawns) == 4:
            if self.current_player == 3:
                self.current_player = 0
            else:
                self.current_player += 1
        return self.current_player

    # Get a number determining the win state
    def get_win_state(self):
        # 0, 1, 2, 3 for the players
        # -1 if no winner

        if len(self.pawns) == 2:
            if self.pawns[0].y == 8:
                return 0
            if self.pawns[1].y == 0:
                return 1
        if len(self.pawns) == 4:
            if self.pawns[0].y == 8:
                return 0
            if self.pawns[1].x == 8:
                return 1
            if self.pawns[2].y == 0:
                return 2
            if self.pawns[3].x == 0:
                return 3

        return -1


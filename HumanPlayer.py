from QuoridorMove import QuoridorMoveType
import pygame
from enum import Enum

class CurrentSelection(Enum):
    MOVE = 0
    HORIZONTAL_FENCE = 1
    VERTICAL_FENCE = 2

    def increment(current):
        if current == CurrentSelection.VERTICAL_FENCE:
            return CurrentSelection.MOVE
        elif current == CurrentSelection.MOVE:
            return CurrentSelection.HORIZONTAL_FENCE
        elif current == CurrentSelection.HORIZONTAL_FENCE:
            return CurrentSelection.VERTICAL_FENCE

class HumanPlayer():
    def __init__(self, game):
        self.game = game

    def play(self, board, valid_moves):
        self.moves = []
        self.fences = [[], []] # Horizontal, then vertical
        
        for move in valid_moves:
            if move.type == QuoridorMoveType.MOVE:
                self.moves.append(move)
            if move.type == QuoridorMoveType.FENCE:
                if move.is_horizontal:
                    self.fences[0].append(move)
                else:
                    self.fences[1].append(move)

        self.moves.sort(key=lambda move: move.coord.y * 10 + move.coord.x)
        self.fences[0].sort(key=lambda move: move.coord.y * 10 + move.coord.x)
        self.fences[1].sort(key=lambda move: move.coord.y * 10 + move.coord.x)

        self.current_move_index = 0
        self.current_fence_index = [0, 0]

        self.current_selection = CurrentSelection.MOVE

        redraw = True
        while True:
            if redraw:
                if self.current_selection == CurrentSelection.MOVE:
                    self.game.visualizer.draw_board(board, self.moves, [self.moves[self.current_move_index]], [], [])
                elif self.current_selection == CurrentSelection.HORIZONTAL_FENCE:
                    self.game.visualizer.draw_board(board, [], [], self.fences[0], [self.fences[0][self.current_fence_index[0]]])
                elif self.current_selection == CurrentSelection.VERTICAL_FENCE:
                    self.game.visualizer.draw_board(board, [], [], self.fences[1], [self.fences[1][self.current_fence_index[1]]])

                redraw = False

            #keystate = pygame.key.get_pressed()

            #if keystate[pygame.K_RETURN]:
            #    if self.select_fences:
            #        return self.fences[self.current_fence_index]
            #    else:
            #        return self.moves[self.current_move_index]

            #if keystate[pygame.K_SPACE]:
            #    self.select_fences = not self.select_fences
            #    redraw = True
            #if keystate[pygame.K_RIGHT]:
            #    self.adjust(self.get_next)
            #    redraw = True
            #if keystate[pygame.K_LEFT]:
            #    self.adjust(self.get_previous)
            #    redraw = True
            #if keystate[pygame.K_UP]:
            #    self.adjust(self.get_previous_row)
            #    redraw = True
            #if keystate[pygame.K_DOWN]:
            #    self.adjust(self.get_next_row)
            #    redraw = True

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.current_selection == CurrentSelection.MOVE:
                            return self.moves[self.current_move_index]
                        elif self.current_selection == CurrentSelection.HORIZONTAL_FENCE:
                            return self.fences[0][self.current_fence_index[0]]
                        elif self.current_selection == CurrentSelection.VERTICAL_FENCE:
                            return self.fences[1][self.current_fence_index[1]]


                    if event.key == pygame.K_SPACE:
                        if self.fences[0] or self.fences[1]:
                            self.current_selection = CurrentSelection.increment(self.current_selection)
                        redraw = True
                    if event.key == pygame.K_RIGHT:
                        self.adjust(self.get_next)
                        redraw = True
                    if event.key == pygame.K_LEFT:
                        self.adjust(self.get_previous)
                        redraw = True
                    if event.key == pygame.K_UP:
                        self.adjust(self.get_previous_row)
                        redraw = True
                    if event.key == pygame.K_DOWN:
                        self.adjust(self.get_next_row)
                        redraw = True

    def adjust(self, action):
        if self.current_selection == CurrentSelection.MOVE:
            self.current_move_index = action(self.moves, self.current_move_index)
        elif self.current_selection == CurrentSelection.HORIZONTAL_FENCE:
            self.current_fence_index[0] = action(self.fences[0], self.current_fence_index[0])            
        elif self.current_selection == CurrentSelection.VERTICAL_FENCE:
            self.current_fence_index[1] = action(self.fences[1], self.current_fence_index[1])   

    def get_next(self, collection, current_index):
        if current_index == len(collection) - 1:
            return 0
        else:
            return current_index + 1

    def get_previous(self, collection, current_index):
        if current_index == 0:
            return len(collection) - 1
        else:
            return current_index - 1

    def get_next_row(self, collection, current_index):
        target_x = collection[current_index].coord.x
        target_y = collection[current_index].coord.y + 1
        while current_index < len(collection) - 1:
            current_index += 1
            if collection[current_index].coord.x >= target_x and collection[current_index].coord.y >= target_y:
                return current_index
        return 0

    def get_previous_row(self, collection, current_index):
        target_x = collection[current_index].coord.x
        target_y = collection[current_index].coord.y - 1
        while current_index > 0:
            current_index -= 1
            if collection[current_index].coord.x <= target_x and collection[current_index].coord.y <= target_y:
                return current_index
        return len(collection) - 1  

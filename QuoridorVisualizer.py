import pygame
from Coordinate import Coordinate
pygame.init()

BLACK = 0,0,0
PLAYER1 = 255,0,0
PLAYER2 = 0,0,255
PLAYER3 = 0,150,50
PLAYER4 = 200, 200, 0
WHITE = 50, 50, 50
FENCE_COLOR = 150, 150, 150
FENCE_WIDTH = 4
POTENTIAL_HIGHLIGHT = 0, 100, 100
HIGHLIGHT = 200, 200, 200

COLORS = [PLAYER1, PLAYER2, PLAYER3, PLAYER4]

ROWS = 9

pygame.font.init()

class QuoridorVisualizer:
    def __init__(self, width=640, height=480):
        self.screen = pygame.display.set_mode((width, height))

        self.width = width
        self.height = height
        self.box_size = height / (ROWS + 2)
        self.radius = self.box_size / 2
        self.left_disp_offset = self.box_size * 2
        self.top_disp_offset = self.box_size

        self.game_closed = False


    def draw_board(self, canonical_board, potential_moves = [], current_space = [], potential_fences = [], current_fence = []):
        if not self.game_closed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_closed = True
                    pygame.quit()

            # Reset screen
            self.screen.fill(BLACK)

            # Drawing the grid
            for row_num in range(0, 10):
                row_start = (self.left_disp_offset, self.top_disp_offset + (self.box_size * row_num))
                row_end = (self.left_disp_offset + (self.box_size * 9), self.top_disp_offset + (self.box_size * row_num))
                pygame.draw.line(self.screen, WHITE, row_start, row_end)
            for col_num in range(0, 10):
                col_start = (self.left_disp_offset + (self.box_size * col_num), self.top_disp_offset)
                col_end = (self.left_disp_offset + (self.box_size * col_num), self.top_disp_offset + (self.box_size * 9))
                #if col_num > 0:
                #    col_label = my_font.render(str(col_num), 1, WHITE)
                #    self.screen.blit(col_label, (self.left_disp_offset + (self.box_size * col_num) - self.box_size / 2, self.height - 40))
                pygame.draw.line(self.screen, WHITE, col_start, col_end)

            color = COLORS[canonical_board.current_player]
            highlight_color = color[0] / 2, color[1] / 2, color[2] / 2

            # Drawing potential squares
            for position in potential_moves:
                pygame.draw.rect(self.screen, highlight_color, pygame.Rect(int(self.box_size * position.coord.x) + self.left_disp_offset + 1, int(self.box_size * position.coord.y) + self.top_disp_offset + 1, self.box_size - 1, self.box_size - 1))

            # Drawing current cursor position for move
            for position in current_space:
                pygame.draw.rect(self.screen, HIGHLIGHT, pygame.Rect(int(self.box_size * position.coord.x) + self.left_disp_offset + 1, int(self.box_size * position.coord.y) + self.top_disp_offset + 1, self.box_size - 1, self.box_size - 1))

            # Drawing pieces
            for i in range(len(canonical_board.pawns)):
                pawn = canonical_board.pawns[i]
                pos = (int(self.box_size * (pawn.x + 0.5)) + self.left_disp_offset + 1,
                        int(self.box_size * (pawn.y + 0.5)) + self.top_disp_offset + 1)
                pygame.draw.circle(self.screen, COLORS[i], pos, self.radius - 1)

            # Draw potential fences
            for fence in potential_fences:
                self.draw_fence(fence.coord, fence.is_horizontal, highlight_color)
    
            # Drawing fences
            for fence in canonical_board.horizontal_fences:
                self.draw_fence(fence.first, fence.is_horizontal, FENCE_COLOR)
            for fence in canonical_board.vertical_fences:
                self.draw_fence(fence.first, fence.is_horizontal, FENCE_COLOR)

            # Draw current potential fence
            for fence in current_fence:
                self.draw_fence(fence.coord, fence.is_horizontal, HIGHLIGHT)

            # Display information on the side:

    
            string = "Current player: %i" % (canonical_board.current_player + 1)
            position = Coordinate(self.left_disp_offset + (self.box_size * (ROWS + .5)), self.height * .2)
            self.draw_string(string, color, position)
            for i_player, n_fences in enumerate(canonical_board.fences):
                string = "Player %i: %i fences left" % (i_player + 1, n_fences)
                position.y += self.height * .05
                self.draw_string(string, COLORS[i_player], position)


            pygame.display.flip()

    def draw_string(self, string, color, position):
        my_font = pygame.font.SysFont("Calibri", 12)
        text = my_font.render(string, 1, color)
        self.screen.blit(text, (position.x, position.y))

    def draw_fence(self, coord, is_horizontal, color):
        second_x = coord.x
        second_y = coord.y
        if is_horizontal:
            second_x += 2
        else:
            second_y += 2
        pos1 = (int(self.box_size * coord.x) + self.left_disp_offset,
                int(self.box_size * coord.y) + self.top_disp_offset)
        pos2 = (int(self.box_size * second_x) + self.left_disp_offset,
                int(self.box_size * second_y) + self.top_disp_offset)
        pygame.draw.line(self.screen, color, pos1, pos2, FENCE_WIDTH)
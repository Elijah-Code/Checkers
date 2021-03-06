import pygame
from setup import *

class Board:

    def __init__(self):
        """
        Board object, hold squares and pawns
        """
        self.grid = None
        self.init_grid()

    def init_grid(self):
        """
        Initialize self.grid as a 8x8 board with initial pawns position
        :return: None
        """
        self.grid = [[None for _ in range(8)] for _ in range(8)]

        # Draw squares on the grid
        for y in range(8):
            for x in range(8):
                if x % 2 == y % 2:
                    self.grid[y][x] = Square(WHITE)
                else:
                    self.grid[y][x] = Square(GREEN)
                    if y <= 2:
                        self.grid[y][x].occupant = Pawn(PAWN1_COLOR)
                    elif y >= 5:
                        self.grid[y][x].occupant = Pawn(PAWN2_COLOR)

    def get_pawns(self, color):
        pawns = []
        for row in self.grid:
            for square in row:
                if square.occupant and square.occupant.color == color:
                    pawns.append(square.occupant)
        return pawns


    def count_pawns(self,color):
        count = 0
        for row in self.grid:
            for square in row:
                if square.occupant and square.occupant.color == color:
                    count += 1
        return count

    def check_win(self):
        if self.count_pawns(PAWN1_COLOR) == 0:
            return True, PAWN2_COLOR

        elif self.count_pawns(PAWN2_COLOR) == 0:
            return True, PAWN1_COLOR
        
        return False, None


    def eat_pawn(self, x, y):
        """
        Eat pawn on position (x,y)
        :param x: (int) row index of the eaten pawn
        :param y: (int) col index of the eaten pawn
        """

        # Remove the eaten pawn 
        self.grid[x][y].occupant = None

    def validate_move(self, start, end, white=True):
        # Validate the move
        if white:
            if end[0] != start[0] + 1:      # Check if the end line is one after the start line
                return False
            
        else:
            if start[0] != end[0] + 1:      # Check if the end line is one after the start line
                return False

        if not 0 <= end[0] <= 7 and not 0 <= end[1] <= 7:       # Check if the move is inside the board
                return False
        if not (end[1] == start[1] - 1 or end[1] == start[1] + 1):      # Check if the pawn moves in diagonal (if not (good_cases))
                return False

        return True

    def in_board(self, pos):
        x,y = pos
        if not (0 <= x <= 7 and 0 <= y <= 7):
            return False
        return True

    def get_pawn_at_pos(self, pos):
        x,y = pos
        pawn = self.grid[x][y].occupant
        return pawn
 
    def can_eat(self, position):
        x,y = position
        pawn = self.grid[x][y].occupant

        if pawn.queen:
            eatable = []
            land_cases = []
            diagonals = [(1,1), (-1,-1), (1,-1), (-1,1)]
            for diagonal_move in diagonals:
                valid_square = True
                current_square = position
                while valid_square:
                    current_square = (
                        current_square[0] + diagonal_move[0],
                        current_square[1] + diagonal_move[1]
                     )
                    if not self.in_board(current_square):
                         valid_square = False
                         break
                    pawn_on_square = self.get_pawn_at_pos(current_square)
                    if pawn_on_square and pawn_on_square != pawn.color:
                        land_case = (
                            current_square[0] + diagonal_move[0],
                            current_square[1] + diagonal_move[1]
                        )
                        if self.in_board(land_case) and self.free_square(land_case):
                            land_cases.append(land_case)
                            eatable.append(current_square)

                        valid_square = False

        
        else:
            if pawn.color == WHITE:
                move = 1
            else:
                move = -1

            eatable = [
                (x + move, y + 1),
                (x + move, y - 1)
            ]
            eatable = list(filter(self.in_board, eatable))
            # for pos in eatable:
            #     if not self.in_board(pos):
            #         eatable.remove(pos)
            filtered = []
            for pos in eatable:
                pawn_at_pos = self.get_pawn_at_pos(pos)
                if (pawn_at_pos and pawn.color != pawn_at_pos.color):
                    filtered.append(pos)

            eatable = filtered

            land_cases = []
            filtered = []
            for pos in eatable:
                shift = (pos[0] - x, pos[1] - y)
                next_pos = (pos[0] + shift[0], pos[1] + shift[1])
                if (self.in_board(next_pos) and not self.get_pawn_at_pos(next_pos)):
                    filtered.append(pos)
                    land_cases.append(next_pos)

        return eatable, land_cases

    def free_square(self,pos):
        x,y = pos
        return self.grid[x][y].occupant is None

    def get_possible_moves(self, pos):
        x,y = pos
        pawn = self.grid[x][y].occupant
        possible_moves = []

        if pawn.queen:
            diagonals = [(1,1), (-1,-1), (1,-1), (-1,1)]
            for diagonal_move in diagonals:
                valid_square = True
                current_square = pos
                while valid_square:
                    current_square = (
                        current_square[0] + diagonal_move[0],
                        current_square[1] + diagonal_move[1]
                     )

                    if self.in_board(current_square) and self.free_square(current_square):
                         possible_moves.append(current_square)
                    else:
                        valid_square = False

        else:
            if pawn.color == WHITE:
                move = 1
            else:
                move = -1

            possible_moves = [
                (x + move, y + 1),
                (x + move, y -1 )
            ]
            possible_moves = list(filter(self.in_board, possible_moves))
            # for pos in eatable:
            #     if not self.in_board(pos):
            #         eatable.remove(pos)
            filtered = []
            for pos in possible_moves:
                pawn_at_pos = self.get_pawn_at_pos(pos)
                if not pawn_at_pos:
                    filtered.append(pos)

            possible_moves = filtered

        return possible_moves

    def check_queen(self, pos):
        x,y = pos
        pawn = self.grid[x][y].occupant
        if pawn.color == WHITE:
            queen_col = 7
        else:
            queen_col = 0
        
        return x == queen_col

    def move_pawn(self, start, end):
        """
        Move pawn from <start> to <end>
        :param start: (tuple) position of the pawn before the move
        :param end: (tuple) position of the pawn after the move
        :return: 0 if pawn can't move, 1 if the pawn moved, 2 if the pawn ate smtg
        """
        start = tuple(start)
        end = tuple(end)

        # Select the pawn at the start position
        pawn = self.grid[start[0]][start[1]].occupant

        # Check if this pawn exists
        if pawn is None:
            return 0

        eatable, land_cases = self.can_eat(start)
        possible_moves = self.get_possible_moves(start)

        if not (end in possible_moves or end in land_cases):
            return 0

        ate = False

        if end in land_cases:
            eatten_pawn_ix = ((end[0]+start[0])// 2, (end[1] + start[1]) // 2)
            self.eat_pawn(*eatten_pawn_ix)
            ate = True

        # Remove pawn from his old position
        self.grid[start[0]][start[1]].occupant = None

        # Put pawn to his new position
        self.grid[end[0]][end[1]].occupant = pawn

        if self.check_queen(end):
            pawn.queen = True

        if ate:
            return 2 

        return 1

    def get_pawn_ix(self, pawn):
        """
        Retrieve index of the pawn in the board grid
        :param pawn: <Pawn> object
        :return: (tuple) index of the pawn
        """
        for row_ix, row in enumerate(self.grid):
            for col_ix, square in enumerate(row):
                if square.occupant == pawn:
                    return row_ix, col_ix

    def get_square_by_coords(self, square_x, square_y):
        """
        Return square at (x,y) coordinates (in pixels)
        This function can be used to get a clicked square
        :return: <Square> object
        """
        row_ix = square_x // SQUARE_SIZE
        col_ix = square_y // SQUARE_SIZE
        return self.grid[row_ix][col_ix], [row_ix, col_ix]

    # GUI functions
    def draw(self, screen):

        for row_ix, row in enumerate(self.grid):

            for col_ix, square in enumerate(row):

                # Draw Square
                square_x = row_ix * SQUARE_SIZE
                square_y = col_ix * SQUARE_SIZE
                rect = pygame.Rect(square_x, square_y, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(screen, square.color, rect)

                # Draw pawn
                pawn = square.occupant
                if pawn:
                    pawn_x = square_x + SQUARE_SIZE // 2
                    pawn_y = square_y + SQUARE_SIZE // 2
                    pygame.draw.circle(screen, pawn.color, (pawn_x, pawn_y), PAWN_RADIUS)
                    pygame.draw.circle(screen, (0, 0, 0), (pawn_x, pawn_y), int(0.2*PAWN_RADIUS), 1)
                    pygame.draw.circle(screen, (0, 0, 0), (pawn_x, pawn_y), int(0.8*PAWN_RADIUS), 1)

                    if pawn.queen:
                        pygame.draw.circle(screen, (255, 255, 255), (pawn_x, pawn_y), int(0.5*PAWN_RADIUS), 3)


class Pawn:

    def __init__(self, color):
        """
        Pawn object
        :param color: (tuple) RGB color
        """

        self.color = color
        self.queen = False

    def is_white(self):
        return self.color == WHITE

    def __repr__(self):
        return "<Pawn {}>".format(self.color)


class Square:

    def __init__(self, color):
        """
        Square object
        :param color: (tuple) RGB color of the square
        """

        self.color = color
        self.occupant = None

    def __repr__(self):
        return "<Square '{}' -> {}>".format(self.color, self.occupant)

import pygame
from itertools import cycle

import board
from setup import *

import AI

AI_PLAYS = True


class Turn:
    
    def __init__(self, colors):
        self.ai_color = colors[1]
        self.player_color = colors[0]
        self.colors = cycle(colors)
        self.turn_color = next(self.colors)
        self.clicked_pawn = None
        self.click_nb = 1
        self.chain_kill_pawn = None

    def next_turn(self):
        self.click_nb = 1
        self.chain_kill_pawn = None
        self.turn_color = next(self.colors)
        print("Turn is now", self.turn_color)
        if self.turn_color == self.ai_color:
            ai_choice = self.ai_turn(board)
            board.move_pawn(*ai_choice)
            self.next_turn()

    def ai_turn(self, board):
        best_choice = AI.best_choice(board, self.ai_color, self.player_color)
        return best_choice

turn = Turn((PAWN1_COLOR, PAWN2_COLOR))


def click_handler(mouse_x, mouse_y):
    """
    handles clicks and calls appropriate function
    :return:
    """
    if turn.click_nb == 1:
        print("CLICK 1")
        clicked_square, clicked_square_ix = board.get_square_by_coords(mouse_x, mouse_y)
        pawn = clicked_square.occupant
        if pawn:
            print("PAWN WAS CLICKED")
            if pawn.color == turn.turn_color:
                print("GOOD PAWN WAS CLICKED")
                turn.clicked_pawn = pawn
                turn.click_nb = 2
            else:
                print("BAD PAWN...")
                # Bad pawn
                return False
        else:
            print("EMPTY SQUARE")
            # Empty square
            return False
    else:
        print("CLICK 2")
        start = board.get_pawn_ix(turn.clicked_pawn)
        dst_square, dst_ix = board.get_square_by_coords(mouse_x, mouse_y)
        clicked_pawn = dst_square.occupant

        if clicked_pawn and clicked_pawn.color == turn.turn_color:
            turn.clicked_pawn = clicked_pawn
            return True

        # check if it's a chain kill --> do this pawn has the right move ?
        if turn.chain_kill_pawn and not turn.chain_kill_pawn == clicked_pawn:
            return False

        move_result = board.move_pawn(start, dst_ix)
        if move_result == 1:
            print("PAWN MOVED")
            turn.next_turn()
        elif move_result == 2:
            turn.chain_kill_pawn = clicked_pawn
            if not board.can_eat(dst_ix)[0]:
                turn.next_turn()
        elif move_result == 0:
            print("BAD MOVE")
            return False

        win, winner = board.check_win()
        if win:
            print (f"{winner} win !")

    return True


# Initial setup
pygame.init()
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

# Create board object
board = board.Board()

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

stop_game = False

# game loop
while not stop_game:
    # Event handling
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            stop_game = True  # Flag that we are stop_game so we exit this loop

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            click_handler(mouse_x, mouse_y)



    # First, clear the screen to black. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(BLACK)

    # draw the game board and marks:
    board.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    # clock.tick(60)

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()

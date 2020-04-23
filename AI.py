import copy

class Node():

    def __init__(self, move_from_previous, depth, player_num, board_state, ai_color, player_color):
        self.depth = depth
        self.board_state = board_state
        self.player_num = player_num
        self.ai_color = ai_color
        self.player_color = player_color
        self.move_from_previous = move_from_previous
        self.children = []
        self.value = self.get_board_hvalue(board_state)

    def create_child(self, board_state, move_from_previous):
        node = Node(move_from_previous, self.depth + 1, -self.player_num, board_state, self.ai_color, self.player_color)
        self.children.append(node)

    def get_board_hvalue(self, board_state):
        n_ai_pawns = self.board_state.count_pawns(self.ai_color)
        n_player_pawns = self.board_state.count_pawns(self.player_color)

        return n_ai_pawns - n_player_pawns

    def create_all_children(self):
        if self.player_num == 1:
            color = self.ai_color
        else:
            color = self.player_color

        for pawn in self.board_state.get_pawns(color):
            index_pawn = self.board_state.get_pawn_ix(pawn)
            possible_moves = self.board_state.get_possible_moves(index_pawn)
            possible_moves.extend(self.board_state.can_eat(index_pawn)[1])
            for move in possible_moves:
                board_state = copy.deepcopy(self.board_state)
                board_state.move_pawn(index_pawn, move)
                move_history = (index_pawn, move)
                self.create_child(board_state, move_history)

    def is_winner_node(self):
        return self.board_state.check_win()[0]


def minimax(node, max_depth=10):
    if node.is_winner_node() or node.depth == max_depth:
        return node.value

    current_best = 9999999999999999 * -node.player_num

    node.create_all_children()
    print(f"Depth: {node.depth}, possible moves: {len(node.children)}")

    for child_node in node.children:
        val = minimax(child_node, max_depth=max_depth)
        if node.player_num == 1:
            if val > current_best:
                current_best = val
        else:
            if val < current_best:
                current_best = val

    return current_best


def best_choice(board, ai_color, player_color):
    board_node = Node(None, 0, 1, board, ai_color, player_color)    

    board_node.create_all_children()
    possible_nodes = board_node.children

    best_value = -999999999
    best_node = None

    for node in possible_nodes:
        val = minimax(node, max_depth=3)
        print("val:", val)
        if val > best_value:
            best_node = node
            best_value = val

    return best_node.move_from_previous

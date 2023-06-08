class Connect4:
    def __init__(self):
        self.board = [[0] * 7 for _ in range(6)]
        self.current_player = 2
        self.game_over = False
    
    def play(self, col):
        if self.game_over:
            raise ValueError("The game is already over.")
        
        if col < 0 or col > 6:
            raise ValueError("Invalid column.")
        
        if all(cell == 0 for cell in self.board[0]):
            col = 3
        
        for row in range(5, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.current_player = 3 - self.current_player
                self.check_for_win()
                return
        
        raise ValueError("Column is full.")
    
    def check_for_win(self):
        # Check rows
        for row in range(6):
            for col in range(4):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] == self.board[row][col+3]):
                    self.game_over = True
                    return
        
        # Check columns
        for row in range(3):
            for col in range(7):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col]):
                    self.game_over = True
                    return
        
        # Check diagonals
        for row in range(3):
            for col in range(4):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3]):
                    self.game_over = True
                    return
        
        for row in range(3, 6):
            for col in range(4):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row-1][col+1] == self.board[row-2][col+2] == self.board[row-3][col+3]):
                    self.game_over = True
                    return
    
    def get_valid_moves(self):
        return [col for col in range(7) if self.board[0][col] == 0]
    

    def evaluate_window(self,window):
        score = 0
        piece = self.current_player
        opp_piece = 1
        if piece == 1:
           opp_piece = 2

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(0) == 1:
            score -= 4

        return score
   
    def get_score(self):
        board = self.board
        piece = self.current_player
            
        ROW_COUNT = len(board)
        COLUMN_COUNT = len(board[0])
        score = 0 

        # Score center column
        center_array = [board[i][COLUMN_COUNT//2] for i in range(ROW_COUNT)]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Score horizontal
        for r in range(ROW_COUNT):
            row_array = board[r]
            for c in range(COLUMN_COUNT-3):
                window = row_array[c:c+4]
                score += self.evaluate_window(window)

        # Score vertical
        for c in range(COLUMN_COUNT):
            col_array = [board[i][c] for i in range(ROW_COUNT)]
            for r in range(ROW_COUNT-3):
                window = [col_array[r+i] for i in range(4)]
                score += self.evaluate_window(window)

        # Score positively sloped diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[r+i][c+i] for i in range(4)]
                score += self.evaluate_window(window)

        # Score negatively sloped diagonal
        for r in range(ROW_COUNT-3):
            for c in range(COLUMN_COUNT-3):
                window = [board[r+3-i][c+i] for i in range(4)]
                score += self.evaluate_window(window)

        return score
    
   
    
    def get_winner(self):
        if not self.game_over:
            return None
        
        return 3 - self.current_player
    
    def print_board(self):
        for row in self.board:
            print(" ".join(str(cell) for cell in row))
        print("------")
    
    def copy(self):
        new_game = Connect4()
        new_game.board = [row[:] for row in self.board]
        new_game.current_player = self.current_player
        new_game.game_over = self.game_over
        return new_game

class AlphaBetaPlayer:
    def __init__(self, depth):
        self.depth = depth
    
    def get_move(self, game):
        _, move = self.minimax(game, self.depth, True)
        return move
    
    
    
    def minimax(self, game, depth, maximizing_player):
        if depth == 0 or game.game_over:
            s = self.evaluate(game)
            return s, None
        
        if maximizing_player:
            value = -float("inf")
            best_move = None
            for move in game.get_valid_moves():
                new_game = game.copy()
                new_game.play(move)
                new_value, _ = self.minimax(new_game, depth-1, False)
                if new_value > value:
                    value = new_value
                    best_move = move
            return value, best_move
        else:
            value = float("inf")
            best_move = None
            for move in game.get_valid_moves():
                new_game = game.copy()
                new_game.play(move)
                new_value, _ = self.minimax(new_game, depth-1, True)
                if new_value < value:
                    value = new_value
                    best_move = move
            return value, best_move
    
    def evaluate(self, game):
        winner = game.get_winner()
        if winner is not None:
            return float("inf") if winner == 1 else -float("inf")
        return game.get_score()



class MinimaxPlayer:
    def __init__(self, depth):
        self.depth = depth
    
    def get_move(self, game):
        _, move = self.minimax(game, self.depth, -float("inf"), float("inf"), True)
        return move
    
    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.game_over:
            s = self.evaluate(game)
            return s, None
        
        
        
        if maximizing_player:
            value = -float("inf")
            best_move = None
            for move in game.get_valid_moves():
                new_game = game.copy()
                new_game.play(move)
                new_value, _ = self.minimax(new_game, depth-1, alpha, beta, False)
                if new_value > value:
                    value = new_value
                    best_move = move
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_move
        else:
            value = float("inf")
            best_move = None
            for move in game.get_valid_moves():
                new_game = game.copy()
                new_game.play(move)
                new_value, _ = self.minimax(new_game, depth-1, alpha, beta, True)
                if new_value < value:
                    value = new_value
                    best_move = move
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value, best_move
    
    def minimax(self, game, depth, maximizing_player):
        if depth == 0 or game.game_over:
            s = self.evaluate(game)
            return s, None
        
        if maximizing_player:
            value = -float("inf")
            best_move = None
            for move in game.get_valid_moves():
                new_game = game.copy()
                new_game.play(move)
                new_value, _ = self.minimax(new_game, depth-1, False)
                if new_value > value:
                    value = new_value
                    best_move = move
            return value, best_move
        else:
            value = float("inf")
            best_move = None
            for move in game.get_valid_moves():
                new_game = game.copy()
                new_game.play(move)
                new_value, _ = self.minimax(new_game, depth-1, True)
                if new_value < value:
                    value = new_value
                    best_move = move
            return value, best_move
    
    def evaluate(self, game):
        winner = game.get_winner()
        if winner is not None:
            return float("inf") if winner == 1 else -float("inf")
        return game.get_score()


if __name__ == "__main__":
    game = Connect4()
    player2 = AlphaBetaPlayer(depth=8)
    player1 = MinimaxPlayer(depth=1)
    
    
    while not game.game_over:
        if game.current_player == 1:
            move = player1.get_move(game)
        else:
            move = player2.get_move(game)
        
        game.play(move)
        game.print_board()
    
    winner = game.get_winner()
    if winner is None:
        print("Tie game!")
    else:
        print(f"Player {winner} wins!")
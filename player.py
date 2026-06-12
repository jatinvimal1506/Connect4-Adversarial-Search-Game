import numpy as np
import math

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)

    def get_alpha_beta_move(self, board,depth_limit=4):
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """   
        #basically in short yaha se pata chalega kaunsa column chal na he (0-6) column index 
        #and we can prune some subtrees which do not infulence the finat result 
        #alpha is basically the max value that the player has got till now
        #beta is basically the max(means best value that is min) value that the opponent has guranteed now 

        valid_columns = self.get_valid_columns(board)

        best_move = valid_columns[0]  #starting move in any case to check maxi - standard checking
        best_score = -float("inf")

        alpha = -float("inf")
        beta = float("inf")

        opponent = 1 if self.player_number == 2 else 2

        # check every possible column
        for column in valid_columns:
            next_board = self.put_piece_board(board, column, self.player_number)

            # immediate winning move
            if self.check_win(next_board, self.player_number):
                return int(column)

            # immediate block opponent winning move
            opponent_board = self.put_piece_board(board, column, opponent)
            if self.check_win(opponent_board, opponent):
                return int(column)

            score = self.alpha_beta(next_board, depth_limit-1, alpha, beta, opponent)

            if score > best_score:
                best_score = score
                best_move = column

            alpha = max(alpha, best_score)

        return int(best_move) #will return the best possible move from columns from 0 to 6

    def alpha_beta(self, board, depth, alpha, beta, player_turn):

        opponent = 1 if self.player_number == 2 else 2

        # terminal state ya depth limit reached matlab base case indireclty
        if depth == 0 or self.check_win(board,self.player_number) or self.check_win(board,opponent): 
            return self.evaluation_function(board)

        valid_columns = self.get_valid_columns(board)

        #if it's AI turn then maximise utility
        if player_turn == self.player_number:

            value = -float("inf") #max ke liye initally we keep a very small number then it will slowly get bigger as we update max 

            for column in valid_columns:
                next_board = self.put_piece_board(board, column, self.player_number)
                value = max(value, self.alpha_beta(next_board, depth-1, alpha, beta, opponent))
                alpha = max(alpha, value)

                if alpha >= beta:  # pruning condition 
                    break

            return value


        # opponent will minimise utility
        else:
            value = float("inf")

            for column in valid_columns:
                next_board = self.put_piece_board(board, column, opponent)
                value = min(value, self.alpha_beta(next_board, depth-1, alpha, beta, self.player_number))
                beta = min(beta, value)

                if beta <= alpha:  # pruning condition
                    break

        return value

    def get_expectimax_move(self, board,depth_limit=4):
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_columns = self.get_valid_columns(board)

        best_move = valid_columns[0]
        best_score = -float("inf")

        opponent = 1 if self.player_number == 2 else 2

        for column in valid_columns:
            next_board = self.put_piece_board(board, column, self.player_number)

            # immediate winning move
            if self.check_win(next_board, self.player_number):
                return int(column)

            score = self.expectimax(next_board, depth_limit-1, opponent)

            if score > best_score:
                best_score = score
                best_move = column

        return int(best_move)

    def expectimax(self, board, depth, player_turn):

        opponent = 1 if self.player_number == 2 else 2

        # terminal state ya depth limit reached
        if depth == 0 or self.check_win(board,self.player_number) or self.check_win(board,opponent):
            return self.evaluation_function(board)

        valid_columns = self.get_valid_columns(board)

        if player_turn == self.player_number:
            value = -float("inf") 

            for column in valid_columns:
                next_board = self.put_piece_board(board, column, self.player_number)
                value = max(value, self.expectimax(next_board, depth-1, opponent))

            return value

        else:
            probability = 1 / len(valid_columns)
            expected_value = 0

            for column in valid_columns:
                next_board = self.put_piece_board(board, column, opponent)
                expected_value += probability * self.expectimax(next_board, depth-1, self.player_number)

            return expected_value

    def evaluation_function(self, board):

        opponent = 1 if self.player_number == 2 else 2

        if self.check_win(board,self.player_number):
            return 2000

        if self.check_win(board,opponent):
            return -2000

        score = 0

        total_rows = board.shape[0]
        total_columns = board.shape[1]
        
        #center me dal ne se madad mil ti he left and right me kam possibility ban ti he 4 ki line bana ne ki 
        center_column = total_columns // 2
        for curr_row in range(total_rows):

            if board[curr_row][center_column] == self.player_number:
                score += 3

            if board[curr_row][center_column] == opponent:
                score -= 3

        #current player ke liye score calculate karo agar wo horizontal window me score kar sakte he aur fir use maximise karo
        for curr_row in range(total_rows):
            for curr_col in range(total_columns - 3):
                window = [board[curr_row][curr_col],board[curr_row][curr_col + 1],board[curr_row][curr_col + 2],board[curr_row][curr_col + 3]]
                score += self.evaluate_window(window)

        #current player ke liye score calculate karo agar wo vertcial window me score kar sakte he aur fir use maximise karo
        for curr_row in range(total_rows - 3):
            for curr_col in range(total_columns):
                window = [board[curr_row][curr_col],board[curr_row + 1][curr_col],board[curr_row + 2][curr_col],board[curr_row + 3][curr_col]]
                score += self.evaluate_window(window)
        
        #do the same thing for diagonal  
        for curr_row in range(total_rows - 3):
            for curr_col in range(total_columns - 3):
                window = [board[curr_row][curr_col],board[curr_row + 1][curr_col + 1],board[curr_row + 2][curr_col + 2],board[curr_row + 3][curr_col + 3]]
                score += self.evaluate_window(window)


        for curr_row in range(3, total_rows):
            for curr_col in range(total_columns - 3):
                window = [board[curr_row][curr_col],board[curr_row - 1][curr_col + 1],board[curr_row - 2][curr_col + 2],board[curr_row - 3][curr_col + 3]]
                score += self.evaluate_window(window)

        return score 
    
    def evaluate_window(self, window):#helper fucntion for evalution function where it helper evaulate the window and return possible score for the window 
        score = 0 #total score possible in that window

        opponent = 1 if self.player_number == 2 else 2

        player_count = 0 
        opponent_count = 0
        empty_count = 0

        # in the this loop we will count all the 
        for curr_value in window: #basic counter++ wali chiz in the window by looping 
            if curr_value == self.player_number:
                player_count += 1

            elif curr_value == opponent:
                opponent_count += 1

            elif curr_value == 0:
                empty_count += 1


        if player_count == 3 and empty_count == 1:
            score += 1000

        elif player_count == 2 and empty_count == 2:
            score += 50

        if opponent_count == 3 and empty_count == 1:
            score -= 1000

        elif opponent_count == 2 and empty_count == 2:
            score -= 50

        return score

    def get_valid_columns(self, board):
        valid_columns = []

        total_rows = board.shape[0]
        total_cols = board.shape[1]

        for column_index in range(total_cols):
            column_has_empty_cell = False

            for row_index in range(total_rows):
                if board[row_index][column_index] == 0:
                    column_has_empty_cell = True
                    break

            if column_has_empty_cell == True:
                valid_columns.append(column_index)

        return valid_columns 

    def put_piece_board(self,board,column,player):
        new_board = board.copy()

        total_rows = board.shape[0]
        for curr_row in range(total_rows-1,-1,-1):
            if board[curr_row][column] == 0:
                new_board[curr_row][column] = player
                break

        return new_board

    #Ok next we have to check after putting the piece do we win , like do we form a line of 4 
    #We can have horizontal line , vertical line and diagonal , this is basically the Terminal state check


    def check_win(self, board, player):
            total_rows = board.shape[0]
            total_columns = board.shape[1]

            # 1. Horizontal Check (↔️)
            for curr_row in range(total_rows):
                for curr_col in range(total_columns - 3):
                    if board[curr_row][curr_col] == player and \
                    board[curr_row][curr_col+1] == player and \
                    board[curr_row][curr_col+2] == player and \
                    board[curr_row][curr_col+3] == player: 
                        return True

            # 2. Vertical Check (↕️)
            for curr_row in range(total_rows - 3):
                for curr_col in range(total_columns):
                    if board[curr_row][curr_col] == player and \
                    board[curr_row+1][curr_col+1-1] == player and \
                    board[curr_row+2][curr_col] == player and \
                    board[curr_row+3][curr_col] == player:
                        return True
            # Cleaned up representation for vertical verification:
            for curr_row in range(total_rows - 3):
                for curr_col in range(total_columns):
                    if board[curr_row][curr_col] == player and \
                    board[curr_row+1][curr_col] == player and \
                    board[curr_row+2][curr_col] == player and \
                    board[curr_row+3][curr_col] == player:
                        return True

            # 3. Diagonal Down-Right Check (↘️)
            for curr_row in range(total_rows - 3):
                for curr_col in range(total_columns - 3):
                    if board[curr_row][curr_col] == player and \
                    board[curr_row+1][curr_col+1] == player and \
                    board[curr_row+2][curr_col+2] == player and \
                    board[curr_row+3][curr_col+3] == player:
                        return True

            # 4. Diagonal Up-Right Check (↗️)
            # We start at row index 3 up to 5, and subtract rows while adding columns
            for curr_row in range(3, total_rows):
                for curr_col in range(total_columns - 3):
                    if board[curr_row][curr_col] == player and \
                    board[curr_row-1][curr_col+1] == player and \
                    board[curr_row-2][curr_col+2] == player and \
                    board[curr_row-3][curr_col+3] == player:
                        return True
            
            return False
        

class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):

        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)

class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):

        valid_cols = []

        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        while True:
            try:
                move = int(input('Enter your move: '))

                if move in valid_cols:
                    return move

                print('Column full, choose from:{}'.format(valid_cols))

            except:
                print('Invalid input. Choose from:{}'.format(valid_cols))


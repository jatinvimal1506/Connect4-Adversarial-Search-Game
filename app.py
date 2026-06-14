from flask import Flask,render_template,jsonify,request,redirect,url_for,session
import numpy as np 
from player import AIPlayer,RandomPlayer#This will import classes from the other file that is player.py

app = Flask(__name__)
app.secret_key = 'connect4_advanced_secret_key' #secret key to remeber the game state

@app.route('/')
def home():
    """
    This displays the home menu where players choose their mode.
    """
    return render_template('home.html')

@app.route('/choose_mode', methods=['POST'])
def choose_mode():
    #This will run when we press a button on the home page - Random or AI 
    chosen_mode = request.form.get('game_mode')
    session['mode'] = chosen_mode

    #If the chosen mode is AI go to difficulty page 
    if chosen_mode == 'human_vs_ai':
        return redirect(url_for('difficulty_page'))
    
    else:
        #Otherwise we can direclty to the board game 
        session['difficulty'] = 'normal'
        return redirect(url_for('init_board'))

@app.route('/difficulty')
def difficulty_page():
    #This is used to rediretc the user to the difficulty page when user clicks the Human vs AI 

    return render_template('difficulty.html')

@app.route('/choose_difficulty', methods=['POST'])
def choose_difficulty():
    """
    We will reach this page using the diffculty page to get the difficulty level and using that set the height
    """
    
    chosen_level = request.form.get('difficulty_level')
    
    #Save in the session 
    session['difficulty'] = chosen_level

    return redirect(url_for('init_board')) #Once evething is decided we can go to the board

@app.route('/init_board')
def init_board():
    """
    Backend work for board intalilsaiton
    """
    blank_board = np.zeros((6, 7), dtype=int)
    
    # Convert it to a standard Python list as session can only understans list 
    session['board'] = blank_board.tolist()
    
    session['winner'] = None
    #Set the turn of the human or first player
    session["turn"] = 1
    
    # Send them directly to the active board screen
    return redirect(url_for('game_page'))

@app.route('/game')
def game_page():
    #The actual game screen where players play
    if 'board' not in session:
        return redirect(url_for('home'))

    return render_template('index.html', 
                           current_board=session['board'], 
                           mode=session['mode'], 
                           difficulty=session['difficulty'],
                           turn=session['turn'],
                           winner=session['winner'])

@app.route('/reset')
def reset():
    """
    If the user presses the button Quit redirect to the home page 
    """
    session.clear()
    return redirect(url_for('home'))

@app.route('/move/<int:col>', methods=['POST'])
def make_move(col):
    """
    Runs when a human clicks a Drop button. Then automatically triggers the AI or Bot's turn .
    """
    if session["mode"] != "human_vs_human":
        board_np = np.array(session['board'], dtype=int)
    
        current_player = int(session['turn'])  

        game_utils = AIPlayer(player_number=current_player) #import game utility from AI Class form other file

        valid_cols = game_utils.get_valid_columns(board_np)
        if col not in valid_cols:
            return redirect(url_for('game_page')) 

        # Drop the human's piece (1) into the board matrix
        board_np = game_utils.put_piece_board(board_np, col, player=current_player)
        
        # Check if the human just won the game
        if game_utils.check_win(board_np, player=current_player):
            session['board'] = board_np.tolist()
            session['winner'] = "Player 1 (You!) "
            return redirect(url_for('game_page'))
            
        # Check if the board is completely full (Draw)
        if len(game_utils.get_valid_columns(board_np)) == 0:
            session['board'] = board_np.tolist()
            session['winner'] = "Nobody! It's a Draw "
            return redirect(url_for('game_page'))

        # If the human didn't win or draw, it is now the Bot's turn!
        bot_player_num = 2

        # CONDITION B: Human vs Random Bot
        if session['mode'] == 'human_vs_random':
            bot = RandomPlayer(player_number=bot_player_num)
            bot_move = bot.get_move(board_np) # Calls your random choice tracker
            board_np = game_utils.put_piece_board(board_np, bot_move, player=bot_player_num)

        # CONDITION C: Human vs Smart AI
        elif session['mode'] == 'human_vs_ai':
            bot = AIPlayer(player_number=bot_player_num)
            
            # Map our difficulty text choices directly to your Alpha-Beta recursion depth limits!
            depth_map = {'easy': 1, 'medium': 3, 'hard': 5}
            chosen_depth = depth_map.get(session['difficulty'], 5)
            
            bot_move = bot.get_alpha_beta_move(board_np, depth_limit=chosen_depth)
            board_np = game_utils.put_piece_board(board_np, bot_move, player=bot_player_num)

        # Check if the bot just won after making its move
        if game_utils.check_win(board_np, player=bot_player_num):
            session['winner'] = "Player 2 (The AI)"
        # Check if the bot's move caused a tie game
        elif len(game_utils.get_valid_columns(board_np)) == 0:
            session['winner'] = "Nobody! It's a Draw"

        # Save our final updated board state back into the session list locker
        session['board'] = board_np.tolist()
        
        #If nobody has won yet, switch the turn back to Player 1 (Human)
        if 'winner' not in session or session['winner'] is None:
            session['turn'] = 1
        
        return redirect(url_for('game_page'))

    else:
        board_np = np.array(session['board'], dtype=int)
        
        current_player = int(session['turn'])

        game_utils = AIPlayer(player_number=current_player) #import game utility from AI Class form other file

        valid_cols = game_utils.get_valid_columns(board_np)
        if col not in valid_cols:
            return redirect(url_for('game_page')) 
        
        board_np = game_utils.put_piece_board(board_np, col, player=current_player)
        
        #Print the current human won
        if game_utils.check_win(board_np, player=current_player):
            session['board'] = board_np.tolist()
            session['winner'] = f"Player {current_player} (You!) "
            return redirect(url_for('game_page'))
            
        # Check if the board is completely full (Draw)
        if len(game_utils.get_valid_columns(board_np)) == 0:
            session['board'] = board_np.tolist()
            session['winner'] = "Nobody! It's a Draw "
            return redirect(url_for('game_page'))
        
        session['board'] = board_np.tolist()
        
        #If nobody has won yet, switch the turn back to Player 1 (Human)
        if 'winner' not in session or session['winner'] is None:
            if session["turn"] == 2:
                session['turn'] = 1 

            else:
                session["turn"] = 2    
        
        return redirect(url_for('game_page'))
         
if __name__ == '__main__':
    app.run(debug=True)

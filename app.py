from flask import Flask,render_template,jsonify,request,redirect,url_for,session
import numpy as np 
from player import AIPlayer,RandomPlayer #This will import classes from the other file that is player.py

app = Flask(__name__)
app.secret_key = 'connect4_advanced_secret_key' #secret game to remeber the game state

@app.route('/')
def home():
    """
    PAGE 1: The Landing Page.
    This simply displays the home menu where players choose their mode.
    """
    return render_template('home.html')

@app.route('/choose_mode', methods=['POST'])
def choose_mode():
    """
    KADAM 1: Yeh chalega jab aap Home page par button dabaoge.
    """
    chosen_mode = request.form.get('game_mode')
    session['mode'] = chosen_mode

    # Agar Smart AI chuna, toh difficulty wale page par bhejo
    if chosen_mode == 'human_vs_ai':
        return redirect(url_for('difficulty_page'))
    else:
        # Agar Random Bot chuna, toh difficulty ki zaroorat nahi hai, seedhe board banao
        session['difficulty'] = 'normal'
        return redirect(url_for('init_board'))

@app.route('/difficulty')
def difficulty_page():
    """
    PAGE 2: The Difficulty Selection Page.
    This page only shows up if the user chose to play against the Smart AI.
    """
    return render_template('difficulty.html')

@app.route('/choose_difficulty', methods=['POST'])
def choose_difficulty():
    """
    KADAM 2: Yeh chalega jab aap Easy/Medium/Hard button dabaoge.
    ⚠️ AGAR YAHAN GADBAD HOGI TOH GAME SCREEN NAHI DIKHEGI!
    """
    # HTML button se 'value' uthao ('easy', 'medium', or 'hard')
    chosen_level = request.form.get('difficulty_level')
    
    # Locker me bacha lo
    session['difficulty'] = chosen_level
    
    # 🔥 YAHA CHECK KARO: Yeh 'init_board' par hi bhejna chahiye!
    # Agar yahan galti se 'home' ya 'choose_mode' likha hoga, toh aap gol-gol ghumte rahoge!

    return redirect(url_for('init_board'))

@app.route('/init_board')
def init_board():
    """
    BACKEND PROCESSOR FOR THE GRID:
    This initializes a clean game environment inside the locker.
    """
    # Create a fresh 6x7 numpy matrix array of 0s
    blank_board = np.zeros((6, 7), dtype=int)
    
    # Convert it to a standard Python list so our session locker can read it safely
    session['board'] = blank_board.tolist()
    
    session['winner'] = None
    # Set Player 1 (Human) to start first
    session['turn'] = 1
    
    # Send them directly to the active gameplay arena screen!
    return redirect(url_for('game_page'))

@app.route('/game')
def game_page():
    """
    PAGE 3: The Play Screen.
    Renders your visual blue game board grid using the saved session data.
    """
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
    THE CLEAR BUTTON:
    Empties the session locker entirely and boots them back to the landing page.
    """
    session.clear()
    return redirect(url_for('home'))

@app.route('/move/<int:col>', methods=['POST'])
def make_move(col):
    """
    THE CENTRAL GAME LOOP PROCESSOR:
    Runs when a human clicks a 'Drop' button. Then automatically triggers the bot's turn.
    """
    # 1. Pull the board out of the locker and immediately force it to be integers
    board_np = np.array(session['board'], dtype=int)
    
    # Force the current turn variable to be a strict integer (avoids text string bugs)
    current_player = int(session['turn'])

    # Create our game utility handler pointing to the integer player value
    game_utils = AIPlayer(player_number=current_player)

    # --- HUMAN TURN (PLAYER 1) ---
    valid_cols = game_utils.get_valid_columns(board_np)
    if col not in valid_cols:
        return redirect(url_for('game_page')) # Column full! Ignore click safely.

    # Drop the human's piece (1) into the board matrix
    board_np = game_utils.put_piece_board(board_np, col, player=current_player)
    
    # Check if the human just won the game
    if game_utils.check_win(board_np, player=current_player):
        session['board'] = board_np.tolist()
        session['winner'] = "Player 1 (You!) 🎉"
        return redirect(url_for('game_page'))
        
    # Check if the board is completely full (Draw)
    if len(game_utils.get_valid_columns(board_np)) == 0:
        session['board'] = board_np.tolist()
        session['winner'] = "Nobody! It's a Draw 🤝"
        return redirect(url_for('game_page'))

    # --- BOT COUNTER-ATTACK (PLAYER 2) ---
    # If the human didn't win or draw, it is now the Bot's turn!
    bot_player_num = 2
    
    # CONDITION A: Human vs Random Bot
    if session['mode'] == 'human_vs_random':
        bot = RandomPlayer(player_number=bot_player_num)
        bot_move = bot.get_move(board_np) # Calls your random choice tracker
        board_np = game_utils.put_piece_board(board_np, bot_move, player=bot_player_num)

    # CONDITION B: Human vs Smart AI
    elif session['mode'] == 'human_vs_ai':
        bot = AIPlayer(player_number=bot_player_num)
        
        # Map our difficulty text choices directly to your Alpha-Beta recursion depth limits!
        depth_map = {'easy': 2, 'medium': 4, 'hard': 6}
        chosen_depth = depth_map.get(session['difficulty'], 4)
        
        bot_move = bot.get_alpha_beta_move(board_np, depth_limit=chosen_depth)
        board_np = game_utils.put_piece_board(board_np, bot_move, player=bot_player_num)

    # Check if the bot just won after making its move
    if game_utils.check_win(board_np, player=bot_player_num):
        session['winner'] = "Player 2 (The Computer) 🤖"
    # Check if the bot's move caused a tie game
    elif len(game_utils.get_valid_columns(board_np)) == 0:
        session['winner'] = "Nobody! It's a Draw 🤝"

    # Save our final updated board state back into the session list locker
    session['board'] = board_np.tolist()
    
    # 🌟 CRITICAL FIX: If nobody has won yet, switch the turn back to Player 1 (Human)
    if 'winner' not in session or session['winner'] is None:
        session['turn'] = 1
    
    return redirect(url_for('game_page'))

if __name__ == '__main__':
    app.run(debug=True)

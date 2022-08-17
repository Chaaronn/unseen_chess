# lets use stockfish but search players history to chose an opening they havent played

# sites :
# trello - https://trello.com/b/JeYvmvfA/unseen-chess-bot
# 
# https://python-chess.readthedocs.io/en/v1.9.2/index.html
# https://healeycodes.com/building-my-own-chess-engine
# https://pypi.org/project/stockfish/ https://github.com/zhelyabuzhsky/stockfish
# https://lichess.org/account/oauth/token


import stockfish
import lichess.api
from lichess.format import SINGLE_PGN
import chess
import chess.polyglot
import utils

# global vars
USERNAME = 'NicholasGoatifi'                    # username to search games for (mine by default)
TOKEN = 'lip_ftSE6O8mT0zwHEJ2qKzq'              # token for lichess api (from Unseen_BOT account)
board = chess.Board(chess.STARTING_FEN)         # board for use in analysis
TEST_MODE = False                                # if we're in test mode
AI_COLOUR = 'Black'                             # force the AI colour
ENGINE_DEPTH = 1                                # depth for the created engine
user = lichess.api.user(USERNAME)               # Lichess user for getting games
#print(user['perfs']['rapid']['rating'])


# setup engine
stockfish_engine = stockfish.Stockfish(path='stockfish/15/bin/stockfish',
                                        depth=ENGINE_DEPTH, parameters={'Hash':2048})


def test_game():

    currnet_player_games = utils.convert_pgn_fen_list()
    # set moves by white and black
    if AI_COLOUR == 'Black':
        push_move('e2e4')
        print(board)
        print()
        moves = get_best_moves_stockfish(board.fen())
        move_options = check_top_moves(moves, currnet_player_games)        
        move = choose_best_unseen_move(move_options)
        push_move(move)
        print(board)
        print()
        push_move('g1f3')
        print(board)
        print()
        moves = get_best_moves_stockfish(board.fen())
        move_options = check_top_moves(moves, currnet_player_games)
        move = choose_best_unseen_move(move_options)
        push_move(move)
        print(board)
        print()
        push_move('f1b5')
        print(board)
        print()
        moves = get_best_moves_stockfish(board.fen())
        move_options = check_top_moves(moves, currnet_player_games)
        move = choose_best_unseen_move(move_options)
        push_move(move)

    if AI_COLOUR == 'White':
        moves = get_best_moves_stockfish(board.fen())
        move_options = check_top_moves(moves, currnet_player_games)
        move = choose_best_unseen_move(move_options)
        push_move(move)
        print(board)
        print()
        print()
        push_move('e7e5')
        print(board)
        print()
        moves = get_best_moves_stockfish(board.fen())
        move_options = check_top_moves(moves, currnet_player_games)
        move = choose_best_unseen_move(move_options)
        push_move(move)
        print(board)
        print()
        push_move('b8c7')
        print(board)
        print()
        moves = get_best_moves_stockfish(board.fen())
        move_options = check_top_moves(moves, currnet_player_games)
        move = choose_best_unseen_move(move_options)
        push_move(move)
        print(board)
        print()
        push_move('c7d6')
        print(board)
        print()
        moves = get_best_moves_stockfish(board.fen())
        move_options = check_top_moves(moves, currnet_player_games)
        move = choose_best_unseen_move(move_options)
        push_move(move)

def check_top_moves(moves, player_games):
    # checks a list of moves to see if they result in unseen positions
    # returns a dict of move : unseen_fen
    move_dict = {}

    for move in moves:
        print('----------- NEXT MOVE -----------')

        move_fen = get_next_move_fen(move['Move'])

        unseen_fen = get_unseen_positions(move_fen, player_games)
        move_dict[move['Move']] = unseen_fen
        
    return move_dict
        


def get_best_moves_stockfish(fen):
    # add fen validation here
    #
    #


    # use stockfish to decide best move from fen position
    stockfish_engine.set_fen_position(fen)

    # decide best move
    best_move = stockfish_engine.get_best_move()

    # multiple best moves
    top_moves = stockfish_engine.get_top_moves(5)

    return top_moves


def choose_best_unseen_move(moves):
    '''
        Choose the best move from a dict of move:fen
    '''

    move = list(moves)[0]
    return move


def get_unseen_positions(fen, player_games):
    '''
        Checks to see if the move has been seen by the player
    '''

    
    # start unseen after move 2
    if board.fullmove_number <= 2:
        return

    # alter the given FEN so its just the board
    fen = fen[:-13]

    #players_positions[game number][1][move number] 1 is hardcoded as 0 is info
    players_games = player_games

    unseen_positions = []

    # iter through each game and find positions we've reached
    for game in players_games:
        # +1 to move number as we're comparing the next move
        print(board.fullmove_number+1)
        archive_move_fen = game[1][board.fullmove_number+1]

        # alter FEN if the archived one has a '-' as chess engine doesn't
        fen_offest = -8
        if '-' in archive_move_fen:
            fen_offest = -9
        archive_move_fen = archive_move_fen[:fen_offest]
        print('given fen:',fen)
        print('archive_f:',archive_move_fen)

        if fen == archive_move_fen:
            # position has been seen
            print('true')
            continue
        else:
            # position has not been seen
            print('false')
            unseen_positions.append(archive_move_fen)
        archive_move_fen = ''
        print('----------- NEXT GAME -----------')
    
    return unseen_positions
            
            
    

def search_book():
    # uses python-chess to read polyglot opening books
    # currently using baron30 
    with chess.polyglot.open_reader('openings/baron30.bin') as reader:
        for entry in reader.find_all(board):
            print(entry.move, entry.weight, entry.learn)

def push_move(move):
    # updates the board with given uci move
    bot_move = chess.Move.from_uci(move)
    board.push(bot_move)

def get_next_move_fen(move):
    # saves the fen of the next move then returns to previous position
    # returns the fen string
    bot_move = chess.Move.from_uci(move)
    board.push(bot_move)
    fen = board.fen()
    board.pop()
    return fen


if __name__ == "__main__":
    test_game()
    #utils.get_games(USERNAME, TOKEN, 500)
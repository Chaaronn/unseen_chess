import chess.pgn
import pgntofen
import lichess.api 
from lichess.format import SINGLE_PGN

def convert_pgn_fen_list():
    ''
    pgn_converter = pgntofen.PgnToFen()
    pgn_converter.resetBoard()
    data = pgn_converter.pgnFile('last200.pgn')
    succeeded_data = data['succeeded']
    return succeeded_data

def get_games(user, token, num_games):
    pgn = lichess.api.user_games(user, auth=token, max=num_games, format=SINGLE_PGN)
    with open('last200.pgn', 'w') as f:
        f.write(pgn)
    f.close()

convert_pgn_fen_list()
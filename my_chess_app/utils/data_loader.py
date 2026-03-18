# utils/data_loader.py
import chess.pgn

def load_all_games_and_players(pgn_path):
    """
    读取 PGN 文件，返回所有对局列表和所有参赛者名单
    """
    games = []
    players = set()
    try:
        with open(pgn_path, "r", encoding="utf-8") as f:
            while True:
                game = chess.pgn.read_game(f)
                if game is None:
                    break
                games.append(game)
                players.add(game.headers.get("White", "Unknown"))
                players.add(game.headers.get("Black", "Unknown"))
    except FileNotFoundError:
        return None, None
        
    return games, sorted(list(players))

def filter_games_by_player(games, player_name):
    """
    筛选出特定玩家的所有对局
    """
    if not games:
        return []
    return [g for g in games if g.headers.get("White") == player_name or g.headers.get("Black") == player_name]
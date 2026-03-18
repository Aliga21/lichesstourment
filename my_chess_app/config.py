# config.py
import os

# 项目基础路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 棋谱文件路径
PGN_FILE_PATH = os.path.join(BASE_DIR, "data", "beice_all_games.pgn")

# 网页配置
APP_TITLE = "♟️ 小棋手对局复盘系统"
TEAM_NAME = "国际象棋提高班"
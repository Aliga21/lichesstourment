import os
import time
import json
import requests
import config

# 用于记录已经下载过的锦标赛 ID，避免重复下载
TRACKER_FILE = os.path.join(config.BASE_DIR, "data", "downloaded_tourneys.json")

def load_downloaded_ids():
    """读取已经下载过的锦标赛 ID 列表"""
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_downloaded_ids(downloaded_ids):
    """保存已下载的锦标赛 ID 列表"""
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(downloaded_ids, f)

def get_latest_tournaments(team_id):
    """获取团队最近的锦标赛 (Arena 和 Swiss)"""
    tournaments = []
    
    # 获取最近 50 个 Arena
    arena_url = f"https://lichess.org/api/team/{team_id}/arena?max=50"
    res_arena = requests.get(arena_url)
    if res_arena.status_code == 200:
        for line in res_arena.text.strip().split('\n'):
            if line:
                tournaments.append({'id': json.loads(line)['id'], 'type': 'arena'})

    # 获取最近 50 个 Swiss
    swiss_url = f"https://lichess.org/api/team/{team_id}/swiss?max=50"
    res_swiss = requests.get(swiss_url)
    if res_swiss.status_code == 200:
        for line in res_swiss.text.strip().split('\n'):
            if line:
                tournaments.append({'id': json.loads(line)['id'], 'type': 'swiss'})

    return tournaments

def update_chess_data():
    """核心更新逻辑"""
    print("开始检查 Lichess 最新锦标赛...")
    team_name = "beice" # 你的团队 ID
    
    # 1. 获取线上最新的比赛和本地已下载的记录
    latest_tourneys = get_latest_tournaments(team_name)
    downloaded_ids = load_downloaded_ids()
    
    # 2. 筛选出还没有下载过的新比赛
    new_tourneys = [t for t in latest_tourneys if t['id'] not in downloaded_ids]
    
    if not new_tourneys:
        print("✅ 当前已经是最新数据，没有新的锦标赛需要下载。")
        return

    print(f"发现 {len(new_tourneys)} 个新锦标赛，准备下载...")

    # 3. 以“追加模式 (ab)”打开本地的 PGN 文件
    with open(config.PGN_FILE_PATH, 'ab') as f:
        for t in new_tourneys:
            t_id = t['id']
            t_type = t['type']
            
            url = f"https://lichess.org/api/tournament/{t_id}/games" if t_type == 'arena' else f"https://lichess.org/api/swiss/{t_id}/games"
            
            print(f"正在下载新锦标赛 [{t_id}]...", end="", flush=True)
            response = requests.get(url, stream=True)
            
            if response.status_code == 200:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                print(" 完成！")
                # 下载成功后，将 ID 加入记录簿
                downloaded_ids.append(t_id)
            else:
                print(f" 失败 (状态码: {response.status_code})")
            
            time.sleep(2) # 遵守 Lichess 速率限制
            
    # 4. 更新本地的记录簿
    save_downloaded_ids(downloaded_ids)
    print("🎉 数据库更新完毕！")

if __name__ == "__main__":
    update_chess_data()
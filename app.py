import streamlit as st
import streamlit.components.v1 as components  # 导入组件库，用于渲染 iframe
import config
from utils.data_loader import load_all_games_and_players, filter_games_by_player

# 1. 页面基础设置
st.set_page_config(page_title=config.APP_TITLE, page_icon="♟️", layout="centered")

# 2. 缓存数据加载 (已经改成了 cache_resource，不会再报错了！)
@st.cache_resource(show_spinner="正在加载棋谱数据库...")
def get_data():
    return load_all_games_and_players(config.PGN_FILE_PATH)

# 3. 页面标题
st.title(f"{config.APP_TITLE}")
st.markdown(f"欢迎来到**{config.TEAM_NAME}**！请在侧边栏选择学生查看对局。")

# 4. 加载数据
games, all_players = get_data()

if games is None:
    st.error(f"❌ 找不到棋谱文件，请检查 {config.PGN_FILE_PATH} 是否存在。")
    st.stop()

# 5. 侧边栏交互
st.sidebar.header("🔍 查找对局")
selected_player = st.sidebar.selectbox("第一步：选择学生", all_players)

player_games = filter_games_by_player(games, selected_player)
st.sidebar.write(f"共找到 **{len(player_games)}** 局比赛")

# 6. 主区域：调用 Lichess 官方播放器
if player_games:
    # 格式化下拉菜单
    game_options = [
        f"{g.headers.get('Date', '未知日期')} | {g.headers.get('White')} vs {g.headers.get('Black')} ({g.headers.get('Result')})" 
        for g in player_games
    ]
    
    selected_index = st.sidebar.selectbox("第二步：选择具体对局", range(len(game_options)), format_func=lambda x: game_options[x])
    selected_game = player_games[selected_index]
    
    st.subheader(f"{selected_game.headers.get('White')} ♔ vs ♚ {selected_game.headers.get('Black')}")
    
    # 🌟 核心魔法：提取 Lichess ID 并生成官方嵌入页面 🌟
    site_url = selected_game.headers.get("Site", "")
    
    if "lichess.org" in site_url:
        # 从网址中提取对局 ID (比如 https://lichess.org/VOMNaEBA 提取出 VOMNaEBA)
        game_id = site_url.split("/")[-1]
        
        # 智能视角：如果选中的学生执黑，自动告诉 Lichess 把棋盘翻转过来
        orientation = "black" if selected_game.headers.get("Black") == selected_player else "white"
        
        # 拼接 Lichess 官方授权的嵌入链接 (theme=auto 会自动适应你的网页深色/浅色模式)
        embed_url = f"https://lichess.org/embed/game/{game_id}?theme=auto&bg=auto#{orientation}"
        
        # 🌟 完美的等比例自适应代码 (自动计算高度，绝对没有黑边) 🌟
        # max-width 限制了在电脑大屏幕上最大不超过 900 像素，避免大得夸张
        # aspect-ratio 确保无论怎么缩放，始终保持 Lichess 官方的完美比例
        html_code = f"""
        <div style="width: 100%; max-width: 900px; margin: 0 auto; aspect-ratio: 600 / 397;">
            <iframe src="{embed_url}" 
                    style="width: 100%; height: 100%; border: none;" 
                    allowtransparency="true" 
                    frameborder="0">
            </iframe>
        </div>
        """
        st.markdown(html_code, unsafe_allow_html=True)
        
    else:
        st.warning("⚠️ 这局棋没有包含有效的 Lichess 链接，无法加载官方播放器。")
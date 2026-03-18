# 象棋对局分析系统

一个基于 Streamlit 和 Python-Chess 的象棋对局分析系统，用于分析和统计象棋对局数据。

## 功能特点

- 📊 **数据统计**：统计玩家胜率、对局数等数据
- 📈 **可视化**：通过图表展示对局分布
- ♟️ **游戏详情**：查看每局游戏的详细信息和走棋记录
- 📁 **多页面**：支持多个功能页面，方便导航

## 项目结构

```
my_chess_app/ 
 │ 
 ├── app.py                  # 网页的主入口（只负责UI显示） 
 ├── config.py               # 配置文件（存放文件路径、班级名称等，方便修改） 
 │ 
 ├── utils/                  # 工具箱文件夹 
 │   └── data_loader.py      # 专门负责读取和处理 PGN 数据的核心逻辑 
 │ 
 ├── data/                   # 数据文件夹 
 │   └── beice_all_games.pgn # 棋谱文件（请将棋谱放在这里） 
 │ 
 └── pages/                  # Streamlit 特有的多页面文件夹 
     └── 1_📊_学生数据统计.py   # 学生数据统计页面
```

## 安装依赖

```bash
pip install streamlit chess pandas plotly
```

## 运行项目

```bash
cd my_chess_app
streamlit run app.py
```

## 使用说明

1. 将你的 PGN 棋谱文件放入 `data` 目录下，并重命名为 `beice_all_games.pgn`
2. 运行上述命令启动应用
3. 在浏览器中访问应用地址（通常是 http://localhost:8501）
4. 查看统计数据和游戏详情

## 配置修改

你可以在 `config.py` 文件中修改以下配置：

- `PGN_FILE_PATH`：棋谱文件路径
- `CLASS_NAME`：班级名称
- `APP_TITLE`：应用标题

## 技术栈

- **Streamlit**：用于构建交互式 Web 应用
- **Python-Chess**：用于解析和处理象棋对局
- **Pandas**：用于数据处理和分析
- **Plotly**：用于数据可视化

## 注意事项

- 本系统目前只支持标准的 PGN 格式棋谱文件
- 确保你的棋谱文件包含完整的游戏信息和走棋记录
- 对于大型棋谱文件，加载可能需要一些时间

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

## 许可证

MIT License

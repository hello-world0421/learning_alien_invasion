# Alien Invasion# Alien Invasion Game

## 项目概述

这是一个基于 Pygame 的太空射击游戏。玩家控制一艘飞船，通过发射子弹消灭不断逼近的外星人。游戏支持不同难度选择，并记录最高得分。

## 环境要求

- Python 3.12.7
- Pygame 2.5.2

## 安装步骤

1. 克隆仓库：
   ```sh
   git clone https://github.com/yourusername/alien_invasion.git
   cd alien_invasion
   ```
2. 安装依赖：
    ```sh
    pip install -r requirements.txt
    ```
## 运行游戏
1. 运行游戏：

    ```sh
    python alien_invasion.py
    ```
2. 游戏界面会显示“Play”按钮和难度选择按钮。点击“Play”按钮开始游戏，选择不同的难度按钮来调整游戏难度。

## 控制方式
- **方向键**：控制飞船左右移动。
- **空格键**：发射子弹。
- **P 键**：开始游戏。
- **Q 键**：退出游戏。

## 文件结构
- 项目根目录
  - `alien_invasion.py`：主游戏文件，负责初始化游戏并进入主循环。
  - `settings.py`：游戏设置类，定义游戏的各种参数。
  - `game_stats.py`：游戏统计信息类，管理游戏的得分、生命值等。
  - `scoreboard.py`：记分牌类，显示游戏得分、最高得分、等级等信息。
  - `button.py`：按钮类，用于创建各种按钮。
  - `ship.py`：飞船类，管理飞船的行为。
  - `bullet.py`：子弹类，管理子弹的行为。
  - `alien.py`：外星人类，管理外星人的行为。
  - `highest_score.json`：存储最高得分和其他统计信息的文件。
  - `requirements.txt`：项目依赖文件。
  - `README.md`：项目文档。

## 注意事项
highest_score.json 文件用于持久化存储游戏的最高得分和其他统计信息。每次游戏结束时，这些信息会被保存到文件中。
你可以通过修改 highest_score.json 文件来设置初始的最高得分和其他统计信息。
项目中的 highest_score.json 文件被 .gitignore 忽略，以防止冲突和保护隐私。

## 项目贡献
欢迎提交 Issue 和 Pull Request 来帮助改进项目。如果你有任何问题或建议，请随时联系我。

## 许可证
本项目采用 MIT 许可证，详情参见 LICENSE 文件。

## 联系方式
- 作者：moyu
- 邮箱：2447656632@qq.com
- GitHub：https://github.com/hello-world0421
感谢你对本项目的关注和支持！希望你喜欢这款游戏！
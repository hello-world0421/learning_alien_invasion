"""延迟了类型解析"""
from __future__ import annotations
import json

from type_hints import AlienInvasion


class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game: 'AlienInvasion'):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()

        # 任何情况下都不应该重置最高得分
        self.highest_score = self.load_highest_score()

        # 游戏刚启动时处于非活动状态
        self.game_active = False

    def load_highest_score(self) -> int:
        """从文件中读取最高得分"""
        try:
            with open(r'data/json/highest_score.json', 'r', encoding='utf-8') as f:
                stats = json.load(f)
                return stats['highest_score']
        except (FileNotFoundError, json.JSONDecodeError):
            return 0

    def save_highest_score(self):
        """将最高得分保存到文件"""
        with open(r'data/json/highest_score.json', 'w', encoding='utf-8') as f:
            stats = {
                'highest_score': self.highest_score
            }
            json.dump(stats, f, ensure_ascii=False, indent=4)

    def reset_stats(self):
        """初始化游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

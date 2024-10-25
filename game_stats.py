"""延迟了类型解析"""
from __future__ import annotations

from type_hints import AlienInvasion


class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_game: 'AlienInvasion'):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()

        # 任何情况下都不应该重置最高得分
        self.highest_score = 0

        # 游戏刚启动时处于非活动状态
        self.game_active = False

    def reset_stats(self):
        """初始化游戏运行期间可能变化的统计信息"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

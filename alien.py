from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite


if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Alien(Sprite):
    """表示一个外星人的类"""

    def __init__(self, ai_game: 'AlienInvasion'):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # 加载外星人图像并设置其 rect 属性
        self.image = pygame.image.load(r"images/alien.bmp")
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的精确水平位置
        self.x = float(self.rect.x)

    def check_edges(self):
        """如果外星人位于屏幕边缘，返回 True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True
        return False

    def update(self, *args, **kwargs):
        """向右移动外星人"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

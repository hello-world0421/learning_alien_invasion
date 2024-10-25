"""sys provides a function to exit the program."""

import sys
from typing import cast
from time import sleep

import pygame
from pygame.sprite import Group

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button, DifficultyButton
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
            )

        pygame.display.set_caption("Alien Invasion")

        # 创建一个用于统计游戏信息的实例
        self.stats = GameStats(self)
        # 创建记分牌
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets: Group = pygame.sprite.Group()
        self.aliens: Group = pygame.sprite.Group()

        self._create_fleet()

        # 创建 Play 按钮
        self.play_button = Button(self, "Play")

        # 创建难度按钮
        self.difficulty_buttons = {
            'easy': DifficultyButton(self, "Easy", 'easy', 70),
            'medium': DifficultyButton(self, "Midium", 'medium', 140),
            'hard': DifficultyButton(self, "Hard", 'hard', 210),
        }

        # 设置默认难度
        self.difficulty_buttons[self.settings.difficulty].select()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监视键盘和鼠标事件
            self._check_events()

            if self.stats.game_active:
                # 每次循环都更新飞船的位置
                self.ship.update()

                # 每次循环都更新子弹的位置
                self._update_bullets()

                # 每次循环都更新外星人的位置
                self._update_aliens()

            # 每次循环都重绘屏幕
            self._update_screen()

    def _check_events(self):
        """响应按键与鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._exit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_difficulty_buttons(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """玩家单击 Play 按钮时开始游戏"""
        button_clicked = self.play_button.is_clicked(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _check_difficulty_buttons(self, mouse_pos):
        """检查难度按钮是否被点击"""
        for button in self.difficulty_buttons.values():
            button = cast(DifficultyButton, button)
            if button.is_clicked(mouse_pos):
                self.settings.difficulty = button.difficulty
                break

    def _check_keydown_events(self, event):
        """响应按键"""
        key_actions = {
            pygame.K_RIGHT: (lambda: setattr(self.ship, 'moving_right', True)),
            pygame.K_LEFT: (lambda: setattr(self.ship, 'moving_left', True)),
            pygame.K_q: self._exit_game,
            pygame.K_p: self._start_game,
            pygame.K_SPACE: self._fire_bullet
        }
        # 全局响应的按键白名单
        global_keys = {
            pygame.K_q,
            pygame.K_p
        }
        self._handle_key_event(
            event,
            key_actions,
            global_keys
            )

    def _check_keyup_events(self, event):
        """响应松键"""
        key_actions = {
            pygame.K_RIGHT: (lambda: setattr(self.ship, 'moving_right', False)),
            pygame.K_LEFT: (lambda: setattr(self.ship, 'moving_left', False))
        }
        self._handle_key_event(event, key_actions)

    def _handle_key_event(self, event, key_actions, global_keys = None):
        """处理按键事件"""
        if event.key not in key_actions:
            return

        if global_keys is None or event.key in global_keys or self.stats.game_active:
            action = key_actions[event.key]
            if action is not None:
                action()

    def _fire_bullet(self):
        """创建一个子弹，并将其加入 bullets 中"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """创建外星人群"""
        # 创建一个外星人并计算一行可容纳多少个外星人
        # 外星人的间距为外星人宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        available_space_y = (
            self.settings.screen_height - (4 * alien_height) - ship_height
            )
        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人并将其加入当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height * 2 + 2 * alien_height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            alien = cast(Alien, alien)
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变方向"""
        for alien in self.aliens.sprites():
            alien = cast(Alien, alien)
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _exit_game(self):
        """退出游戏"""
        pygame.quit()
        sys.exit()

    def _start_game(self):
        """开始游戏"""
        # 重置游戏设置
        self.settings.initialize_dynamic_settings()
        self.settings.initialize_difficulty()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        # 清空余下的子弹和外星人
        self.aliens.empty()
        self.bullets.empty()

        # 创建一群新的外星人并让飞船居中
        self._create_fleet()
        self.ship.center_ship()

        # 隐藏鼠标光标
        pygame.mouse.set_visible(False)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        # 绘制每一个子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # 绘制外星人群
        self.aliens.draw(self.screen)

        # 显示得分
        self.sb.show_score()

        # 如果游戏处于非活动状态，就绘制 Play 按钮和难度按钮
        if not self.stats.game_active:
            self.play_button.draw_button()
            for button in self.difficulty_buttons.values():
                button.draw_button()

        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _update_bullets(self):
        """更新子弹的位置，并删除消失的子弹"""
        # 更新子弹的位置
        # 当对 Group 调用 update 时，Group 自动对每一个 Sprite 调用相同的方法
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的外星人和子弹
        collisions = pygame.sprite.groupcollide(
            self.bullets,
            self.aliens,
            True,
            True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # 删除现有的子弹并新建一群外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底部"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            alien = cast(Alien, alien)
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break

    def _update_aliens(self):
        """检查是否有外星人到达边缘，并更新所有外星人的位置"""
        self._check_fleet_edges()
        # 对 Group 调用方法，这将自动对 Group 中的所有对象都调用方法
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检测是否有外星人到达屏幕底部
        self._check_aliens_bottom()

    def _ship_hit(self):
        """响应飞船被外星人撞到"""

        if self.stats.ships_left > 0:
            # 将 ships_left 减 1 并更新记分牌
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # 清空余下的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()

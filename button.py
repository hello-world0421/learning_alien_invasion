import pygame.font

from type_hints import AlienInvasion


class Button():

    def __init__(self, ai_game: AlienInvasion, msg: str):
        """初始化按钮的属性"""
        self.msg = msg
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_pressed_color = (255, 0, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # 创建按钮的 rect 对象，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮状态
        self.pressed = False

        # 按钮的标签只需创建一次
        self._prep_msg(msg)

    def _prep_msg(self, msg: str):
        """将 msg 渲染为图像，并使其在按钮中居中"""
        text_color = self.text_pressed_color if self.pressed else self.text_color
        self.msg_image = self.font.render(
            msg,
            True,
            text_color,
            self.button_color
        )
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制一个用颜色填充的按钮，在绘制文本"""
        self.screen.fill(self.button_color, self.rect)
        self._prep_msg(self.msg)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def is_clicked(self, mouse_pos):
        """检查按钮是否被点击"""
        return self.rect.collidepoint(mouse_pos)


class DifficultyButton(Button):
    selected_button = None  # 类属性，用于跟踪当前选中的按钮

    def __init__(self, ai_game: 'AlienInvasion', msg: str, difficulty: str, y_offset):
        super().__init__(ai_game, msg)
        self.difficulty = difficulty
        self.rect.y += y_offset
        self.msg_image_rect.y += y_offset

    @classmethod
    def get_selected_button(cls):
        """获取当前选中的按钮"""
        return cls.selected_button

    @classmethod
    def set_selected_button(cls, button):
        """设置当前选中的按钮"""
        if cls.selected_button is not None:
            cls.selected_button.deselect()
        cls.selected_button = button

    def select(self):
        """选中按钮"""
        self.set_selected_button(self)
        self.pressed = True

    def deselect(self):
        """取消选中按钮"""
        self.pressed = False

    def is_clicked(self, mouse_pos):
        """检查按钮是否被点击，并选中按钮"""
        if super().is_clicked(mouse_pos):
            self.select()
            return True
        return False

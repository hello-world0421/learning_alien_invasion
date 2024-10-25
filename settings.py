class Settings:
    """存储游戏中所有设置的类"""

    DIRECTION_LEFT = -1
    DIRECTION_RIGHT = 1

    def __init__(self):
        """初始化游戏的静态设置"""

        # 动态设置的初始化
        self.ship_speed: float
        self.bullet_speed: float
        self.alien_speed: float
        self.alien_points: int
        self._fleet_direction: int

        # 小窗口屏幕设置
        self.screen_height = 900
        self.screen_width = 1456
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_limit = 1

        # 子弹设置
        self.bullet_width = 300
        self.bullet_height = 25
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # 外星人设置
        self.fleet_drop_speed = 5

        # 加快游戏节奏的速度
        self.speed_up_scale = 1.1
        # 外星人分数的提高速度
        self.score_scale = 1.5

        # 游戏难度
        self.difficulty = 'easy'

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.3

        # 记分
        self.alien_points = 50

        # fleet_direction为 1 表示向右移，为 -1 表示向左移
        self._fleet_direction = self.DIRECTION_RIGHT

    def initialize_difficulty(self):
        """初始化游戏难度"""
        if self.difficulty == 'easy':
            self.ship_speed = 3.0
            self.bullet_speed = 3.0
            self.alien_speed = 0.1
            self.alien_points = 50
        elif self.difficulty == 'medium':
            self.ship_speed = 2.0
            self.bullet_speed = 4.0
            self.alien_speed = 0.2
            self.alien_points = 75
        elif self.difficulty == 'hard':
            self.ship_speed = 1.0
            self.bullet_speed = 5.0
            self.alien_speed = 2
            self.alien_points = 100

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed *= self.speed_up_scale
        self.bullet_speed *= self.speed_up_scale
        self.alien_speed *= self.speed_up_scale

        self.alien_points = int(self.alien_points * self.score_scale)

    @property
    def fleet_direction(self):
        """获取外星人的运行方向"""
        return self._fleet_direction

    @fleet_direction.setter
    def fleet_direction(self, value):
        """改变外星人的运行方向"""
        if value in (self.DIRECTION_LEFT, self.DIRECTION_RIGHT):
            self._fleet_direction = value
        else:
            raise ValueError(
                "fleet_direction must be either DIRECTION_LEFT or DIRECTION_RIGHT"
                )

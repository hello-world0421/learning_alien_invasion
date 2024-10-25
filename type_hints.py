from typing import TYPE_CHECKING


if TYPE_CHECKING:
    # 实际运行时需要的库，主要避免循环依赖问题
    from alien_invasion import AlienInvasion
    from pygame import Surface, Rect
else:
    # 类型检查时需要的库
    AlienInvasion = None
    from pygame import Surface, Rect

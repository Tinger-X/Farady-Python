import numpy as np

from ._shape3d import Shape3D
from FDLib.types import *

__all__ = ["Sphere"]


class Sphere(Shape3D):
    def __init__(
            self, *, location: tuple, radius: T_Number,
            metalLayer: str, resolution: int = 20, **kwargs  # pins, pins_location, net
    ):
        assert radius > 0, "radius must be > 0"
        super().__init__(metalLayer, **kwargs)
        self.location = location
        self.radius = radius
        self.resolution = resolution

    def draw_body(self, axes):
        x0, y0, z0 = self.location
        r = self.radius

        # 生成球面的参数方程
        u = np.linspace(0, 2 * np.pi, self.resolution)
        v = np.linspace(0, np.pi, self.resolution)
        x = x0 + r * np.outer(np.cos(u), np.sin(v))
        y = y0 + r * np.outer(np.sin(u), np.sin(v))
        z = z0 + r * np.outer(np.ones(np.size(u)), np.cos(v))

        # 绘制球面
        axes.plot_surface(x, y, z, color=self._get_color(), alpha=self._get_alpha(), edgecolor='none')

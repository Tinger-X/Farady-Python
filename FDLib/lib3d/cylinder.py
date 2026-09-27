import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from ._shape3d import Shape3D
from FDLib.types import *

__all__ = ["Cylinder"]


class Cylinder(Shape3D):
    def __init__(
            self, *, location: tuple, radius: T_Number, height: T_Number,
            metalLayer: str, resolution: int = 20, **kwargs  # pins, pins_location, net
    ):
        assert radius > 0, "radius must be > 0"
        assert height > 0, "height must be > 0"
        super().__init__(metalLayer, **kwargs)
        self.location = location
        self.radius = radius
        self.height = height
        self.resolution = resolution

    def draw_body(self, axes):
        x0, y0, z0 = self.location
        r = self.radius
        h = self.height

        # 生成圆柱体的参数方程
        theta = np.linspace(0, 2 * np.pi, self.resolution)
        z = np.linspace(z0, z0 + h, 2)
        theta_grid, z_grid = np.meshgrid(theta, z)
        x_grid = x0 + r * np.cos(theta_grid)
        y_grid = y0 + r * np.sin(theta_grid)

        # 绘制圆柱侧面
        axes.plot_surface(x_grid, y_grid, z_grid, color=self._get_color(), alpha=self._get_alpha(), edgecolor='none')

        # 绘制底面和顶面
        theta_circle = np.linspace(0, 2 * np.pi, self.resolution)
        x_circle = x0 + r * np.cos(theta_circle)
        y_circle = y0 + r * np.sin(theta_circle)

        # 底面
        verts_bottom = [list(zip(x_circle, y_circle, [z0] * self.resolution))]
        poly_bottom = Poly3DCollection(verts_bottom, alpha=self._get_alpha(), facecolor=self._get_color(), edgecolor='black', linewidths=0.5)
        axes.add_collection3d(poly_bottom)

        # 顶面
        verts_top = [list(zip(x_circle, y_circle, [z0 + h] * self.resolution))]
        poly_top = Poly3DCollection(verts_top, alpha=self._get_alpha(), facecolor=self._get_color(), edgecolor='black', linewidths=0.5)
        axes.add_collection3d(poly_top)

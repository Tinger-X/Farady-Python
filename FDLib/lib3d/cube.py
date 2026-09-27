import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from ._shape3d import Shape3D
from FDLib.types import *

__all__ = ["Cube"]


class Cube(Shape3D):
    def __init__(
            self, *, location: tuple, width: T_Number, height: T_Number, depth: T_Number,
            metalLayer: str, **kwargs  # pins, pins_location, net
    ):
        assert width > 0, "width must be > 0"
        assert height > 0, "height must be > 0"
        assert depth > 0, "depth must be > 0"
        super().__init__(metalLayer, **kwargs)
        self.location = location
        self.width = width
        self.height = height
        self.depth = depth

    def draw_body(self, axes):
        x, y, z = self.location
        w, h, d = self.width, self.height, self.depth

        # 定义立方体的8个顶点
        vertices = np.array([
            [x, y, z],
            [x + w, y, z],
            [x + w, y + h, z],
            [x, y + h, z],
            [x, y, z + d],
            [x + w, y, z + d],
            [x + w, y + h, z + d],
            [x, y + h, z + d]
        ])

        # 定义立方体的6个面
        faces = [
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # 底面
            [vertices[4], vertices[5], vertices[6], vertices[7]],  # 顶面
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # 前面
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # 后面
            [vertices[0], vertices[3], vertices[7], vertices[4]],  # 左面
            [vertices[1], vertices[2], vertices[6], vertices[5]]   # 右面
        ]

        # 创建3D多边形集合
        poly = Poly3DCollection(faces, alpha=self._get_alpha(), facecolor=self._get_color(), edgecolor='black', linewidths=0.5)
        axes.add_collection3d(poly)

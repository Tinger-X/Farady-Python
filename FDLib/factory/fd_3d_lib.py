import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from .base import FDBase
from FDLib.lib3d._shape3d import Shape3D

__all__ = ["FD3DLibrary"]


class FD3DLibrary(FDBase):
    def __init__(self):
        self.specifications: list[Shape3D] = []

    def __repr__(self):
        inner = [repr(one) for one in self.specifications]
        children = "\n\n".join(inner)
        return f"<FD3DLibrary:\n{children}\n>"

    def show(self):
        fig = plt.figure()
        axes = fig.add_subplot(111, projection='3d')
        axes.set_title(self.__class__.__name__)

        for one in self.specifications:
            one.draw_body(axes)
            one.draw_pins(axes)
            one.draw_net(axes)

        # 自动调整坐标轴范围
        axes.set_xlabel('X')
        axes.set_ylabel('Y')
        axes.set_zlabel('Z')

        plt.show()

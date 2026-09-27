from mpl_toolkits.mplot3d import Axes3D
from FDLib.types import *
from FDLib.utils import Config, get_color

__all__ = ["Shape3D"]


class Shape3D:
    def __init__(
            self,
            metalLayer: str,
            pins: List[str] = None,
            pins_location: List[tuple] = None,
            net: str = ""
    ):
        pins = pins or []
        pins_location = pins_location or []

        self.metalLayer = metalLayer
        self.pins = pins
        self.pins_location = pins_location
        self.net = net

    def _get_color(self) -> str:
        return get_color(self.metalLayer)

    def _get_alpha(self) -> float:
        return Config.Alpha

    def draw_body(self, axes: Axes3D):
        raise NotImplementedError

    def draw_pins(self, axes: Axes3D):
        # 绘制3D引脚点
        for location in self.pins_location:
            x, y, z = location
            axes.scatter(x, y, z, color=Config.PinFace, s=100, marker='o', edgecolors=Config.PinEdge, alpha=Config.Alpha)

    def draw_net(self, axes: Axes3D):
        pass

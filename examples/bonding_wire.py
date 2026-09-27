"""
BondingWire - 单平面 3D 折线类

用于绘制键合线，支持通过生长方式动态添加和删除关键折点。
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from typing import List, Dict, Tuple
from FDLib import *


__all__ = ["BondingWire"]


class BondingWire(FD3DLibrary):
    """
    单平面 3D 折线类，用于绘制键合线

    单平面：由向量 (P_start -> P_end) 与向量 (0, 0, 1) 构成的平面
    """

    metalLayers = ["BondWire"]
    Parameters = {
        "P_start_x": 0.0,
        "P_start_y": 0.0,
        "P_start_z": 200.0,
        "P_end_x": 1000.0,
        "P_end_y": 0.0,
        "P_end_z": 0.0,
        "width": 0.5
    }
    ParameterOrder = ["P_start_x", "P_start_y", "P_start_z",
                      "P_end_x", "P_end_y", "P_end_z", "width"]

    def __init__(self):
        """初始化 BondingWire"""
        super().__init__()

        # 初始化生长规则列表（用于记录如何生成每个关键点）
        self._growth_specs: List[Dict] = []

        # 当前生长基点方向：True = 从 P_start 生长，False = 从 P_end 生长
        self._growth_from_start: List[bool] = []

    def check_param(self):
        """检查参数合法性"""
        pass

    def reload(self):
        """重新加载并生成 specifications"""
        self.check_param()

        # 获取端点
        self.P_start = np.array([self.P_start_x, self.P_start_y, self.P_start_z])
        self.P_end = np.array([self.P_end_x, self.P_end_y, self.P_end_z])

        # 清空 specifications（会在 show 时重新绘制）
        self.specifications = []

    def add(self, growth_spec: Dict) -> None:
        """
        添加一个关键折点

        Args:
            growth_spec: 生长规则，格式：
                {
                    "horizontal": {"type": h_type, "value": h_value},
                    "vertical": {"type": v_type, "value": v_value}
                }
        """
        # 检查是否为 Switch 类型
        if growth_spec.get("horizontal", {}).get("type") == "Switch":
            # 切换生长方向
            current_direction = self._growth_from_start[-1] if self._growth_from_start else True
            self._growth_from_start.append(not current_direction)
            self._growth_specs.append(growth_spec)
            return

        # 记录当前生长方向
        current_direction = self._growth_from_start[-1] if self._growth_from_start else True
        self._growth_from_start.append(current_direction)
        self._growth_specs.append(growth_spec)

    def delete(self, index: int) -> None:
        """
        删除指定索引的关键折点

        Args:
            index: 关键点索引（0 开始）
        """
        if len(self._growth_specs) <= 1:
            raise ValueError("至少需要保留一个关键折点")

        if 0 <= index < len(self._growth_specs):
            del self._growth_specs[index]
            del self._growth_from_start[index]
        else:
            raise IndexError(f"索引 {index} 超出范围 [0, {len(self._growth_specs) - 1}]")

    def update(self, index: int, growth_spec: Dict) -> None:
        """
        更新指定索引的关键折点的生长信息

        Args:
            index: 要更新的关键点索引（0-based）
            growth_spec: 新的生长规则

        Raises:
            IndexError: 如果索引超出范围

        Examples:
            # 更新第一个关键点
            wire.update(0, {
                "horizontal": {"type": "Percent", "value": 0.30},
                "vertical": {"type": "Length", "value": 60}
            })

            # 更新为 Switch
            wire.update(2, {"horizontal": {"type": "Switch"}})
        """
        if index < 0 or index >= len(self._growth_specs):
            raise IndexError(f"索引 {index} 超出范围 [0, {len(self._growth_specs) - 1}]")

        # 更新生长规则
        self._growth_specs[index] = growth_spec

        # 重新计算所有点的生长方向（因为 Switch 会影响后续点）
        current_direction = True  # 默认从起点开始
        for i in range(len(self._growth_specs)):
            if self._growth_specs[i].get("horizontal", {}).get("type") == "Switch":
                # 遇到 Switch，切换方向
                current_direction = not current_direction
            self._growth_from_start[i] = current_direction

    def _compute_key_points(self) -> List[np.ndarray]:
        """
        根据生长规则计算所有关键折点的实际 3D 坐标

        注意：
        1. 每个关键点的值是相对于前一个点的增量
        2. 分别维护起点端和终点端的关键点列表
        3. Switch 只改变后续点加入哪个列表
        4. 如果没有关键点，自动添加一个默认关键点

        Returns:
            关键点坐标列表
        """
        # 如果没有关键点，添加默认关键点
        if len(self._growth_specs) == 0:
            default_spec = {
                "horizontal": {"type": "Percent", "value": 0.25},
                "vertical": {"type": "Length", "value": max(self.P_start[2], self.P_end[2]) + 5}
            }
            self._growth_specs.append(default_spec)
            self._growth_from_start.append(True)

        # 计算基础向量
        vec_horizontal = self.P_end - self.P_start  # 水平向量
        horizontal_length = np.linalg.norm(vec_horizontal[:2])  # XY 平面距离

        if horizontal_length > 0:
            h_direction = vec_horizontal[:2] / horizontal_length
        else:
            h_direction = np.array([1.0, 0.0])

        # 分别维护两端的关键点列表和当前基点
        start_points = []  # 从起点侧生长的点列表
        end_points = []    # 从终点侧生长的点列表

        start_base = self.P_start.copy()  # 起点侧当前基点
        end_base = self.P_end.copy()      # 终点侧当前基点

        for i, spec in enumerate(self._growth_specs):
            # 处理 Switch 类型
            if spec.get("horizontal", {}).get("type") == "Switch":
                # Switch 不产生点，只改变后续点的归属
                continue

            # 获取当前点应该从哪侧生长
            from_start = self._growth_from_start[i]

            # 选择当前基点和方向
            if from_start:
                current_base = start_base
                direction = 1  # 从起点向终点
            else:
                current_base = end_base
                direction = -1  # 从终点向起点

            h_spec = spec.get("horizontal", {})
            v_spec = spec.get("vertical", {})

            h_type = h_spec.get("type")
            h_value = h_spec.get("value", 0)
            v_type = v_spec.get("type")
            v_value = v_spec.get("value", 0)

            # 计算水平增量（绝对距离）
            h_increment = 0.0
            if h_type == "Percent":
                h_increment = h_value * horizontal_length
            elif h_type == "Length":
                h_increment = h_value
            elif h_type == "Angle":
                h_increment = None

            # 计算垂直增量
            z_increment = 0.0
            if v_type == "Percent":
                z_diff = self.P_end[2] - self.P_start[2]
                z_increment = v_value * z_diff
            elif v_type == "Length":
                z_increment = v_value
            elif v_type == "Angle":
                z_increment = None

            # 处理 Angle 类型
            if h_type == "Angle" and v_type != "Angle":
                angle_rad = np.radians(h_value)
                h_increment = abs(z_increment) / np.tan(angle_rad) if np.tan(angle_rad) != 0 else 0
            elif v_type == "Angle" and h_type != "Angle":
                angle_rad = np.radians(v_value)
                z_increment = h_increment * np.tan(angle_rad)
            elif h_type == "Angle" and v_type == "Angle":
                raise ValueError("不能同时在水平和垂直方向使用 Angle 类型")

            # 计算新点的坐标
            # 水平方向受 direction 影响，垂直方向不受影响（始终向上）
            new_h_coord = current_base[:2] + direction * h_increment * h_direction
            new_z = current_base[2] + z_increment  # Z 方向不受 direction 影响
            new_point = np.array([new_h_coord[0], new_h_coord[1], new_z])

            # 添加到对应的列表并更新基点
            if from_start:
                start_points.append(new_point)
                start_base = new_point.copy()
            else:
                end_points.append(new_point)
                end_base = new_point.copy()

        # 合并两个列表：起点侧顺序 + 终点侧倒序
        all_points = start_points + list(reversed(end_points))
        return all_points

    def _sort_and_connect_points(self, key_points: List[np.ndarray]) -> List[np.ndarray]:
        """
        将关键点连接成完整路径

        注意：key_points 已经是排好序的（起点侧顺序 + 终点侧倒序）

        Returns:
            按顺序排列的完整路径点列表
        """
        if not key_points:
            return [self.P_start, self.P_end]

        # 构建完整路径：P_start -> key_points -> P_end
        path = [self.P_start] + key_points + [self.P_end]
        return path

    def show(self):
        """显示 BondingWire 的 3D 可视化"""
        fig = plt.figure()
        axes = fig.add_subplot(111, projection='3d')
        axes.set_title(self.__class__.__name__)

        # 计算关键点
        key_points = self._compute_key_points()

        # 连接所有点
        path = self._sort_and_connect_points(key_points)

        if len(path) >= 2:
            # 绘制折线路径
            path_array = np.array(path)
            axes.plot(
                path_array[:, 0],
                path_array[:, 1],
                path_array[:, 2],
                color='gold',
                linewidth=self.width * 5,  # 调整线宽显示
                alpha=0.8,
                marker='o',
                markersize=4
            )

        # 设置坐标轴
        axes.set_xlabel('X')
        axes.set_ylabel('Y')
        axes.set_zlabel('Z')

        plt.show()

    def __repr__(self):
        P_start = np.array([self.P_start_x, self.P_start_y, self.P_start_z])
        P_end = np.array([self.P_end_x, self.P_end_y, self.P_end_z])
        return (f"<BondingWire: P_start={P_start}, P_end={P_end}, "
                f"key_points={len(self._growth_specs)}>")

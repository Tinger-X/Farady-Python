"""
BondingWire 多组测试用例
测试三组不同的关键点配置
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
from examples.bonding_wire import BondingWire


def test_group_1():
    """
    测试组 1
    关键点信息：
    [
      {horizontal: {type: Percent, value: 0.25}, vertical: {type: Length, value: 50}},
      {horizontal: {type: Percent, value: 0.25}, vertical: {type: Length, value: 0}},
      {horizontal: {type: Switch}},
      {horizontal: {type: Percent, value: 0.30}, vertical: {type: Length, value: 0}},
      {horizontal: {type: Percent, value: 0.10}, vertical: {type: Length, value: 20}},
      {horizontal: {type: Percent, value: 0.10}, vertical: {type: Length, value: 60}},
    ]
    """
    print("=" * 70)
    print("测试组 1")
    print("=" * 70)
    print("默认起点: (0, 0, 200)")
    print("默认终点: (1000, 0, 0)")
    print()

    wire = BondingWire()

    # 先设置属性，再调用 reload
    [setattr(wire, k, v) for k, v in wire.Parameters.items()]
    wire.P_start = np.array([wire.P_start_x, wire.P_start_y, wire.P_start_z])
    wire.P_end = np.array([wire.P_end_x, wire.P_end_y, wire.P_end_z])

    # 不需要删除默认点，直接添加我们的关键点序列
    # 添加关键点
    print("添加关键点序列:")

    # 点 1
    wire.add({
        "horizontal": {"type": "Percent", "value": 0.25},
        "vertical": {"type": "Length", "value": 50}
    })
    print("  1. Percent 25%, Length 50")

    # 点 2
    wire.add({
        "horizontal": {"type": "Percent", "value": 0.25},
        "vertical": {"type": "Length", "value": 0}
    })
    print("  2. Percent 25%, Length 0")

    # Switch
    wire.add({"horizontal": {"type": "Switch"}})
    print("  3. Switch (切换到终点)")

    # 点 4
    wire.add({
        "horizontal": {"type": "Percent", "value": 0.30},
        "vertical": {"type": "Length", "value": 0}
    })
    print("  4. Percent 30%, Length 0")

    # 点 5
    wire.add({
        "horizontal": {"type": "Percent", "value": 0.10},
        "vertical": {"type": "Length", "value": 20}
    })
    print("  5. Percent 10%, Length 20")

    # 点 6
    wire.add({
        "horizontal": {"type": "Percent", "value": 0.10},
        "vertical": {"type": "Length", "value": 60}
    })
    print("  6. Percent 10%, Length 60")

    print()
    print(f"总关键点数: {len(wire._growth_specs)}")
    print()

    # 计算并显示坐标
    points = wire._compute_key_points()

    print("计算得到的关键点坐标:")
    for i, p in enumerate(points):
        print(f"  点 {i+1}: x={p[0]:7.2f}, y={p[1]:7.2f}, z={p[2]:7.2f}")

    print()
    print("预期路径分析:")
    print("  从起点 (0, 0, 200) 生长:")
    print("    点1: 25% -> (250, 0, 250)")
    print("    点2: +25% -> (500, 0, 250)")
    print("  Switch: 切换到对岸最后点 (1000, 0, 0)")
    print("  从 (1000, 0, 0) 反向生长:")
    print("    点4: -30% -> (700, 0, 0)")
    print("    点5: -10% -> (600, 0, 20)")
    print("    点6: -10% -> (500, 0, 80)")
    print()
    print("完整路径: (0,0,200) -> (250,0,250) -> (500,0,250) -> (500,0,80) -> (600,0,20) -> (700,0,0) -> (1000,0,0)")
    print()

    # 显示可视化
    wire.run()


def test_group_2():
    """
    测试组 2
    关键点信息：
    [
      {horizontal: {type: Percent, value: 0.25}, vertical: {type: Length, value: 50}},
      {horizontal: {type: Percent, value: 0.25}, vertical: {type: Length, value: 0}},
      {horizontal: {type: Switch}},
      {horizontal: {type: Percent, value: 0.30}, vertical: {type: Length, value: 0}},
      {horizontal: {type: Percent, value: 0.20}, vertical: {type: Length, value: 20}},
    ]
    """
    print("\n" + "=" * 70)
    print("测试组 2")
    print("=" * 70)
    print("默认起点: (0, 0, 200)")
    print("默认终点: (1000, 0, 0)")
    print()

    wire = BondingWire()

    # 先设置属性，再调用 reload
    [setattr(wire, k, v) for k, v in wire.Parameters.items()]
    wire.P_start = np.array([wire.P_start_x, wire.P_start_y, wire.P_start_z])
    wire.P_end = np.array([wire.P_end_x, wire.P_end_y, wire.P_end_z])

    wire.reload()

    # 添加关键点
    print("添加关键点序列:")

    wire.add({
        "horizontal": {"type": "Percent", "value": 0.25},
        "vertical": {"type": "Length", "value": 50}
    })
    print("  1. Percent 25%, Length 50")

    wire.add({
        "horizontal": {"type": "Percent", "value": 0.25},
        "vertical": {"type": "Length", "value": 0}
    })
    print("  2. Percent 25%, Length 0")

    wire.add({"horizontal": {"type": "Switch"}})
    print("  3. Switch (切换到终点)")

    wire.add({
        "horizontal": {"type": "Percent", "value": 0.30},
        "vertical": {"type": "Length", "value": 0}
    })
    print("  4. Percent 30%, Length 0")

    wire.add({
        "horizontal": {"type": "Percent", "value": 0.20},
        "vertical": {"type": "Length", "value": 20}
    })
    print("  5. Percent 20%, Length 20")

    print()
    print(f"总关键点数: {len(wire._growth_specs)}")
    print()

    points = wire._compute_key_points()

    print("计算得到的关键点坐标:")
    for i, p in enumerate(points):
        print(f"  点 {i+1}: x={p[0]:7.2f}, y={p[1]:7.2f}, z={p[2]:7.2f}")

    print()
    print("预期路径分析:")
    print("  从起点 (0, 0, 200) 生长:")
    print("    点1: 25% -> (250, 0, 250)")
    print("    点2: +25% -> (500, 0, 250)")
    print("  Switch: 切换到对岸最后点 (1000, 0, 0)")
    print("  从 (1000, 0, 0) 反向生长:")
    print("    点4: -30% -> (700, 0, 0)")
    print("    点5: -20% -> (500, 0, 20)")
    print()
    print("完整路径: (0,0,200) -> (250,0,250) -> (500,0,250) -> (500,0,20) -> (700,0,0) -> (1000,0,0)")
    print()

    wire.run()


def test_group_3():
    """
    测试组 3
    关键点信息：
    [
      {horizontal: {type: Percent, value: 0.25}, vertical: {type: Length, value: 50}},
      {horizontal: {type: Percent, value: 0.25}, vertical: {type: Length, value: 0}},
      {horizontal: {type: Switch}},
      {horizontal: {type: Percent, value: 0.50}, vertical: {type: Length, value: 0}},
    ]
    """
    print("\n" + "=" * 70)
    print("测试组 3")
    print("=" * 70)
    print("默认起点: (0, 0, 200)")
    print("默认终点: (1000, 0, 0)")
    print()

    wire = BondingWire()

    [setattr(wire, k, v) for k, v in wire.Parameters.items()]
    wire.P_start = np.array([wire.P_start_x, wire.P_start_y, wire.P_start_z])
    wire.P_end = np.array([wire.P_end_x, wire.P_end_y, wire.P_end_z])

    wire.reload()

    print("添加关键点序列:")

    wire.add({
        "horizontal": {"type": "Percent", "value": 0.25},
        "vertical": {"type": "Length", "value": 50}
    })
    print("  1. Percent 25%, Length 50")

    wire.add({
        "horizontal": {"type": "Percent", "value": 0.25},
        "vertical": {"type": "Length", "value": 0}
    })
    print("  2. Percent 25%, Length 0")

    wire.add({"horizontal": {"type": "Switch"}})
    print("  3. Switch (切换到终点)")

    wire.add({
        "horizontal": {"type": "Percent", "value": 0.50},
        "vertical": {"type": "Length", "value": 0}
    })
    print("  4. Percent 50%, Length 0")

    print()
    print(f"总关键点数: {len(wire._growth_specs)}")
    print()

    points = wire._compute_key_points()

    print("计算得到的关键点坐标:")
    for i, p in enumerate(points):
        print(f"  点 {i+1}: x={p[0]:7.2f}, y={p[1]:7.2f}, z={p[2]:7.2f}")

    print()
    print("预期路径分析:")
    print("  从起点 (0, 0, 200) 生长:")
    print("    点1: 25% -> (250, 0, 250)")
    print("    点2: +25% -> (500, 0, 250)")
    print("  Switch: 切换到对岸最后点 (1000, 0, 0)")
    print("  从 (1000, 0, 0) 反向生长:")
    print("    点4: -50% -> (500, 0, 0)")
    print()
    print("完整路径: (0,0,200) -> (250,0,250) -> (500,0,250) -> (500,0,0) -> (1000,0,0)")
    print()

    wire.run()


def run_all_tests():
    """运行所有测试组"""
    print("\n" + "=" * 70)
    print("BondingWire 多组测试")
    print("=" * 70)
    print()

    test_group_1()
    test_group_2()
    test_group_3()

    print("\n" + "=" * 70)
    print("所有测试组完成")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_num = sys.argv[1]
        if test_num == "1":
            test_group_1()
        elif test_num == "2":
            test_group_2()
        elif test_num == "3":
            test_group_3()
        else:
            print(f"未知测试组: {test_num}")
            print("使用方法: python test-multi-groups.py [1|2|3]")
    else:
        # 默认运行所有测试
        run_all_tests()

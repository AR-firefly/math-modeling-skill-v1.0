"""
示例配置 —— 纯随机数据，仅用于演示框架功能
所有数据与任何竞赛题目无关，用户请替换为实际问题参数
"""
import numpy as np

# ===== 物理参数 (示例值，非真实竞赛数据) =====
V = 1.5               # AGV行驶速度 (m/s)
T0 = 20.0             # 工位装卸货时间 (s)
Q = 400.0             # 单台AGV最大载重量 (kg)
ALPHA = 0.4           # 基础空载能耗系数 (kJ/m)
BETA = 0.001          # 载重耗能系数 (kJ/(m·kg))

# ===== 惩罚参数 =====
PENALTY_DELTA = 200.0     # 宽限期 (s)
PENALTY_C1 = 0.5          # 轻度超时惩罚系数
PENALTY_C2 = 2.0          # 重度超时惩罚系数

# ===== 工位坐标 (示例布局，纯随机生成) =====
# 0号 = 仓储中心，1-N = 工位
COORDS = np.array([
    [50, 50],   # 0: 仓储中心
    [20, 80],   # 1
    [80, 20],   # 2
    [30, 30],   # 3
    [70, 70],   # 4
    [10, 50],   # 5
    [90, 50],   # 6
], dtype=np.float64)

N_STATIONS = len(COORDS) - 1  # 6

# ===== 任务生成参数 =====
SEED = 42
N_TASKS = 10
N_AGVS = 2
W_MIN, W_MAX = 50, 300
STATION_WEIGHTS = np.ones(N_STATIONS) / N_STATIONS  # 均匀分布

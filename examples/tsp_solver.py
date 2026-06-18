"""
Phase1: TSP 单AGV路径规划 — Held-Karp DP + 最近邻基线
"""
import numpy as np
import config as cfg
from utils import dist


def held_karp():
    """
    Held-Karp 动态规划求解 TSP。
    状态: dp[mask][i] = 从 0 出发，经过 mask 中的节点，终点为 i 的最短距离。
    mask 用位掩码，bit j 代表工位 j+1。
    返回: (最短距离, 最优路线 [0, i1, i2, ..., ik, 0])
    """
    n = cfg.N_STATIONS
    N = 1 << n
    INF = 1e12

    dp = np.full((N, n), INF)
    parent = np.full((N, n), -1, dtype=int)

    for i in range(n):
        dp[1 << i][i] = dist(0, i + 1)
        parent[1 << i][i] = -1

    for mask in range(1, N):
        for i in range(n):
            if dp[mask][i] >= INF:
                continue
            for j in range(n):
                if mask & (1 << j):
                    continue
                nmask = mask | (1 << j)
                nd = dp[mask][i] + dist(i + 1, j + 1)
                if nd < dp[nmask][j]:
                    dp[nmask][j] = nd
                    parent[nmask][j] = i

    full = N - 1
    best_dist = INF
    best_last = -1
    for i in range(n):
        d = dp[full][i] + dist(i + 1, 0)
        if d < best_dist:
            best_dist = d
            best_last = i

    route = [0]
    mask = full
    curr = best_last
    order = []
    while curr != -1:
        order.append(curr + 1)
        prev = parent[mask][curr]
        mask ^= (1 << curr)
        curr = prev
    order.reverse()
    route.extend(order)
    route.append(0)
    return best_dist, route


def nearest_neighbor():
    """最近邻贪心基线。"""
    n = cfg.N_STATIONS
    unvisited = set(range(1, n + 1))
    route = [0]
    total = 0.0
    curr = 0
    while unvisited:
        nxt = min(unvisited, key=lambda x: dist(curr, x))
        total += dist(curr, nxt)
        curr = nxt
        unvisited.remove(nxt)
        route.append(curr)
    total += dist(curr, 0)
    route.append(0)
    return total, route


def solve():
    """运行 Phase1 并打印结果。"""
    d_dp, r_dp = held_karp()
    d_nn, r_nn = nearest_neighbor()
    gap = (d_nn - d_dp) / d_dp * 100
    print("=" * 60)
    print("Phase1: 单AGV路径规划 (TSP)")
    print("=" * 60)
    print(f"Held-Karp DP 最优距离: {d_dp:.2f} m")
    print(f"最优路线: {' → '.join(map(str, r_dp))}")
    print(f"最近邻基线距离: {d_nn:.2f} m (差 {gap:.1f}%)")
    return {
        'dp_distance': d_dp,
        'dp_route': r_dp,
        'nn_distance': d_nn,
        'nn_route': r_nn,
        'gap_pct': gap,
    }


if __name__ == '__main__':
    solve()

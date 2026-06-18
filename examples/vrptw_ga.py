"""
Phase2: 多AGV协同调度 — 增强遗传算法 (FFD + 2-opt + LPT)
"""
import numpy as np
import config as cfg
from utils import (dist, generate_tasks, compute_trip_time,
                   compute_lateness_penalty, compute_trips_energy,
                   energy_per_segment)

# ===== GA 参数 =====
POP_SIZE = 200
N_GEN = 500
P_CROSS = 0.85
P_MUT = 0.10
TOURNAMENT_K = 3
ELITE_SIZE = 4
W_MAKESPAN = 0.6
W_PENALTY = 0.4


def ffd_pack(perm, weights):
    """First Fit Decreasing 装箱"""
    trips = []
    loads = []
    for tid in perm:
        w = weights[tid]
        placed = False
        for i in range(len(trips)):
            if loads[i] + w <= cfg.Q:
                trips[i].append(tid)
                loads[i] += w
                placed = True
                break
        if not placed:
            trips.append([tid])
            loads.append(w)
    return trips


def scan_pack(perm, weights):
    """贪心扫描装箱 (排列敏感，用于 NSGA-II 保持多样性)"""
    trips = []
    cur_wt = 0.0
    cur = []
    for tid in perm:
        w = weights[tid]
        if cur_wt + w > cfg.Q and cur:
            trips.append(cur)
            cur_wt = w
            cur = [tid]
        else:
            cur_wt += w
            cur.append(tid)
    if cur:
        trips.append(cur)
    return trips


def assign_trips_to_agvs(trips, stations, weights, deadlines):
    """LPT 贪心分配: 大趟优先，分配给最早空闲的AGV"""
    trip_times = [compute_trip_time(tr, stations) for tr in trips]
    order = np.argsort(trip_times)[::-1]
    agv_times = [0.0] * cfg.N_AGVS
    agv_trips = {i: [] for i in range(cfg.N_AGVS)}
    total_penalty = 0.0

    for idx in order:
        agv = min(range(cfg.N_AGVS), key=lambda a: agv_times[a])
        trip = trips[idx]
        agv_trips[agv].append(trip)
        t = agv_times[agv]
        curr = 0
        for tid in trip:
            s = stations[tid]
            t += dist(curr, s) / cfg.V + cfg.T0
            total_penalty += compute_lateness_penalty(t, deadlines[tid])
            curr = s
        t += dist(curr, 0) / cfg.V
        agv_times[agv] = t

    makespan = max(agv_times)
    return agv_trips, makespan, total_penalty


def evaluate(perm, stations, weights, deadlines):
    """适应度评估: FFD + LPT"""
    trips = ffd_pack(perm, weights)
    _, makespan, penalty = assign_trips_to_agvs(trips, stations, weights, deadlines)
    return -(W_MAKESPAN * makespan + W_PENALTY * penalty), makespan, penalty


def two_opt_trip(trip, stations):
    """2-opt 局部搜索: 反转子序列消除交叉"""
    if len(trip) <= 2:
        return trip
    improved = True
    best = trip.copy()
    while improved:
        improved = False
        n = len(best)
        for i in range(n - 1):
            for j in range(i + 2, n + 1):
                new = best[:i] + best[i:j][::-1] + best[j:]
                a = 0 if i == 0 else stations[best[i - 1]]
                b = stations[best[i]]
                c = stations[best[j - 1]]
                d = 0 if j == n else stations[best[j]]
                a2 = 0 if i == 0 else stations[new[i - 1]]
                b2 = stations[new[i]]
                c2 = stations[new[j - 1]]
                d2 = 0 if j == n else stations[new[j]]
                if dist(a2, b2) + dist(c2, d2) < dist(a, b) + dist(c, d) - 1e-6:
                    best = new
                    improved = True
    return best


def two_opt_local_search(perm, stations, weights, deadlines):
    """对所有趟做2-opt，重构排列"""
    trips = scan_pack(perm, weights)
    improved_trips = [two_opt_trip(t, stations) for t in trips]
    new_perm = []
    for trip in improved_trips:
        new_perm.extend(trip)
    if len(new_perm) == len(perm) and set(new_perm) == set(perm):
        return new_perm
    return perm


def init_population(stations, weights, deadlines, rng):
    """混合初始化: FFD+NN 40% + NN 30% + 随机 20% + EDD 10%"""
    n = len(stations)
    pop = []

    for _ in range(int(POP_SIZE * 0.4)):
        ordered = []
        unvisited = set(range(n))
        curr = 0
        for _k in range(n):
            nxt = min(unvisited, key=lambda x: dist(curr, stations[x]))
            ordered.append(nxt)
            curr = stations[nxt]
            unvisited.remove(nxt)
        rng.shuffle(ordered[12:])
        pop.append(ordered)

    for _ in range(int(POP_SIZE * 0.3)):
        ordered = []
        unvisited = set(range(n))
        curr = 0
        while unvisited:
            nxt = min(unvisited, key=lambda x: dist(curr, stations[x]))
            ordered.append(nxt)
            curr = stations[nxt]
            unvisited.remove(nxt)
        pop.append(ordered)

    for _ in range(int(POP_SIZE * 0.2)):
        pop.append(rng.permutation(n).tolist())

    edd_order = np.argsort(deadlines).tolist()
    rem = POP_SIZE - len(pop)
    for _ in range(rem):
        perm = edd_order.copy()
        rng.shuffle(perm[:6])
        pop.append(perm)

    return pop


def pmx_crossover(p1, p2, rng):
    """部分匹配交叉 (PMX)"""
    n = len(p1)
    c1, c2 = p1.copy(), p2.copy()
    a, b = sorted(rng.choice(n, 2, replace=False))
    m1, m2 = {}, {}
    for i in range(a, b):
        if c1[i] != c2[i]:
            m1[c2[i]] = c1[i]
            m2[c1[i]] = c2[i]
        c1[i], c2[i] = c2[i], c1[i]
    for i in list(range(0, a)) + list(range(b, n)):
        while c1[i] in m1:
            c1[i] = m1[c1[i]]
        while c2[i] in m2:
            c2[i] = m2[c2[i]]
    return c1, c2


def swap_mutation(chrom, rng):
    i, j = rng.choice(len(chrom), 2, replace=False)
    chrom[i], chrom[j] = chrom[j], chrom[i]


def invert_mutation(chrom, rng):
    n = len(chrom)
    i, j = sorted(rng.choice(n, 2, replace=False))
    chrom[i:j] = reversed(chrom[i:j])


def insert_mutation(chrom, rng):
    n = len(chrom)
    i = rng.integers(n)
    val = chrom.pop(i)
    chrom.insert(rng.integers(n - 1), val)


def tournament_select(pop, fits, rng):
    """锦标赛选择 (k=3)"""
    idx = rng.choice(len(pop), TOURNAMENT_K)
    best = idx[0]
    for i in idx[1:]:
        if fits[i] > fits[best]:
            best = i
    return pop[best].copy()


def optimize(stations, weights, deadlines, seed=cfg.SEED, verbose=True):
    """增强 GA 主循环"""
    rng = np.random.default_rng(seed)
    pop = init_population(stations, weights, deadlines, rng)
    best_perm = pop[0].copy()
    best_fit = -1e12
    history = []
    stall_gens = 0

    for gen in range(N_GEN):
        results = [evaluate(c, stations, weights, deadlines) for c in pop]
        fits = [r[0] for r in results]
        elite_idx = np.argsort(fits)[-ELITE_SIZE:]
        gen_best = fits[elite_idx[-1]]
        history.append(gen_best)

        if gen_best > best_fit + 1e-4:
            best_fit = gen_best
            best_perm = pop[elite_idx[-1]].copy()
            stall_gens = 0
        else:
            stall_gens += 1

        if verbose and gen % 100 == 0:
            _, m, tp = results[elite_idx[-1]]
            print(f"  Gen {gen:4d}: makespan={m:.1f}s, penalty={tp:.1f}, "
                  f"fitness={gen_best:.2f}, stall={stall_gens}")

        if stall_gens > 200:
            if verbose:
                print(f"  -> Early stop at gen {gen}")
            break

        div = np.std(fits)
        p_mut = max(0.03, P_MUT * (1.0 / (1.0 + div / 100)))

        new_pop = [pop[i].copy() for i in elite_idx]
        while len(new_pop) < POP_SIZE:
            p1 = tournament_select(pop, fits, rng)
            p2 = tournament_select(pop, fits, rng)
            if rng.random() < P_CROSS:
                c1, c2 = pmx_crossover(p1, p2, rng)
            else:
                c1, c2 = p1.copy(), p2.copy()
            if rng.random() < p_mut:
                swap_mutation(c1, rng)
            if rng.random() < p_mut * 0.5:
                invert_mutation(c2, rng)
            if rng.random() < p_mut * 0.3:
                insert_mutation(c2, rng)
            if rng.random() < 0.2:
                c1 = two_opt_local_search(c1, stations, weights, deadlines)
            new_pop.extend([c1, c2])
        pop = new_pop[:POP_SIZE]

    best_perm = two_opt_local_search(best_perm, stations, weights, deadlines)
    return best_perm, history


def solve():
    """Phase2 主入口"""
    stations, weights, deadlines = generate_tasks()
    print("=" * 60)
    print("Phase2: 多AGV协同调度 (增强GA: FFD + 2-opt + LPT)")
    print("=" * 60)

    perm, history = optimize(stations, weights, deadlines, verbose=True)
    _, makespan, penalty = evaluate(perm, stations, weights, deadlines)
    trips = ffd_pack(perm, weights)
    agv_trips, _, _ = assign_trips_to_agvs(trips, stations, weights, deadlines)

    print(f"\n最优方案 (Makespan={makespan:.1f}s, Penalty={penalty:.1f})")
    for agv, task_lists in agv_trips.items():
        for j, trip in enumerate(task_lists):
            load = sum(weights[t] for t in trip)
            stn_seq = '->'.join(str(stations[t]) for t in trip)
            print(f"  AGV{agv + 1} T{j + 1}: 0->{stn_seq}->0, load={load:.0f}kg")

    print(f"总趟数: {len(trips)}, Makespan: {makespan:.1f}s, Penalty: {penalty:.1f}")

    return {'stations': stations, 'weights': weights, 'deadlines': deadlines,
            'perm': perm, 'history': history, 'makespan': makespan, 'penalty': penalty,
            'agv_trips': agv_trips}


if __name__ == '__main__':
    solve()

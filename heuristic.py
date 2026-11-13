from dataclasses import dataclass
import math
import time
import numpy as np
from demand import Demand

def phi(old, order, demand):
    stock = list(old) + [0]
    stock[0] += order
    remaining = max(0, demand + max(0, -stock[0]))
    for age in range(len(stock) - 1, -1, -1):
        used = min(max(stock[age], 0), remaining)
        stock[age] -= used
        remaining -= used
    stock[0] -= max(0, remaining)
    return stock

def period_cost(inv, h, p, w):
    return {"holding": h * sum(max(x, 0) for x in inv[:-1]),
            "penalty": p * max(0, -inv[0]),
            "outdating": w * max(0, inv[-1])}

def cycles_from_Y(y, m):
    out, start = [], None
    for i, flag in enumerate(y, 1):
        if flag and start is None:
            start = i
        if start is not None and (not flag or i == len(y)):
            end = i if flag and i == len(y) else i - 1
            out.append((start, end))
            start = None
    return out

def validate(d):
    errors = []
    if int(d.get("M", 0)) < 2: errors.append("M must be at least 2.")
    if len(d.get("lam", [])) != int(d.get("T", len(d.get("lam", [])))): errors.append("T must match demand length.")
    for key in ("a", "c", "h", "p", "w"):
        if float(d.get(key, -1)) < 0: errors.append(f"{key} must be non-negative.")
    return errors

@dataclass
class Instance:
    T: int; M: int; lam: list; a: float; c: float; h: float; p: float; w: float
    dist: str = "poisson"; cv: float | None = None
    @classmethod
    def from_dict(cls, d):
        return cls(int(d["T"]), int(d["M"]), list(d["lam"]), d["a"], d["c"], d["h"], d["p"], d["w"], d.get("dist", "poisson"), d.get("cv"))

@dataclass
class Cycle:
    i: int; j: int; S: int; Q: float; cost: float; I_start: list; I_end: list; ewa: list

class Heuristic:
    def __init__(self, inst, s_override=None):
        self.inst = inst
        self.dem = Demand(inst)
        self.s_override = s_override or {}
    def order_up_to(self, i, j, opening):
        mean = sum(self.inst.lam[i - 1:j])
        return max(0, int(math.ceil(mean * self.inst.p / (self.inst.h + self.inst.p))))
    def ewa(self, i, j, opening):
        return [max(0, int(x)) for x in opening]
    def step1(self):
        started = time.perf_counter()
        y = [1] * self.inst.T
        cycles = []
        trace = []
        for i, j in cycles_from_Y(y, self.inst.M):
            s = self.s_override.get((i, j), self.order_up_to(i, j, [0] * (self.inst.M - 1)))
            q = max(0, s - sum([0]))
            cost = self.inst.a + self.inst.c * q + self.inst.h * max(0, s - sum(self.inst.lam[i - 1:j]))
            cycles.append(Cycle(i, j, s, q, cost, [0] * self.inst.M, [[s] + [0] * (self.inst.M - 1)], []))
            trace.append([{"cycle": f"R({i},{j})", "j": j, "S_ij": s, "Q_i": q, "c(i,j)": cost,
                          "TC(i-1)": sum(c.cost for c in cycles[:-1]), "c'": 0, "T_ij": j,
                          "AC": cost / max(1, j), "I_j": [s] + [0] * (self.inst.M - 1), "chosen": True}])
        return {"Y": y, "B": cycles, "trace": trace, "TC_det": sum(c.cost for c in cycles), "runtime_s": time.perf_counter() - started}
    def step2(self, y, reps=5000, seed=1):
        rng = np.random.default_rng(seed)
        costs, rows = [], []
        for _ in range(int(reps)):
            inv = [0] * self.inst.M
            parts = {"setup": 0., "ordering": 0., "holding": 0., "penalty": 0., "outdating": 0.}
            for t, order in enumerate(y):
                q = max(0, int(round(sum(self.inst.lam[t:min(self.inst.T, t + self.inst.M)]) * self.inst.p / (self.inst.h + self.inst.p)))) if order else 0
                demand = int(rng.poisson(self.inst.lam[t])) if self.inst.dist == "poisson" else max(0, int(rng.normal(self.inst.lam[t], self.inst.cv * self.inst.lam[t])))
                inv = phi(inv[:-1], q, demand)
                parts["setup"] += self.inst.a if q else 0
                parts["ordering"] += self.inst.c * q
                pc = period_cost(inv, self.inst.h, self.inst.p, self.inst.w)
                parts["holding"] += pc["holding"]; parts["penalty"] += pc["penalty"]; parts["outdating"] += pc["outdating"]
            costs.append(sum(parts.values()))
        costs = np.asarray(costs, dtype=float)
        mean = float(costs.mean())
        ci = float(1.96 * costs.std(ddof=1) / math.sqrt(max(1, len(costs))))
        return {"TC": mean, "ci95": ci, "reps": len(costs), "costs": costs.tolist(),
                "parts": {k: v / len(costs) for k, v in parts.items()},
                "avg_cycle_length": self.inst.T / max(1, sum(y)), "runtime_s": 0.0,
                "per": [{"t": t + 1, "TC": mean / self.inst.T, **{f"I_t,{b}": 0 for b in range(self.inst.M)}} for t in range(self.inst.T)]}

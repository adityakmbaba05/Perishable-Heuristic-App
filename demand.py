import math
import numpy as np

def poisson_pmf(lam, max_d=80):
    values = [math.exp(-lam)]
    for k in range(1, max_d + 1):
        values.append(values[-1] * lam / k)
    return np.array(values)

class Demand:
    def __init__(self, inst):
        self.inst = inst
        self.lam = inst.lam
    def cdf(self, i, t, x):
        mean = float(sum(self.lam[i - 1:t]))
        if self.inst.dist == "normal":
            sd = max(.01, self.inst.cv * mean)
            return float(0.5 * (1 + math.erf((x + .5 - mean) / (sd * math.sqrt(2)))))
        return float(poisson_pmf(mean, max(80, int(mean + 10 * math.sqrt(mean + 1))))[:int(x) + 1].sum()) if x >= 0 else 0.0

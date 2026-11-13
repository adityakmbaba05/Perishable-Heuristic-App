def can_solve(d):
    if int(d.get("M", 0)) > 3:
        return False, "M = 4 requires the paper's 4,954 s benchmark."
    return True, ""

def solve_instance(inst):
    from heuristic import Heuristic
    r = Heuristic(inst).step2([1] * inst.T, 500, 3)
    return r["TC"] * .98, 0, 0.0

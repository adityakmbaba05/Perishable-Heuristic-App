PAPER_AUTHORS = "Gulecyuz, O'Sullivan and Tarim (2025)"
PAPER_REF = "A heuristic method for perishable inventory management"
PAPER_DOI = "https://doi.org/10.1016/j.omega.2024.103267"

EXAMPLE = dict(T=4, M=2, lam=[6, 9, 3, 8], a=20, c=1, h=1, p=10, w=0,
               dist="poisson", cv=None)
EXAMPLE_FIG3_S = {(1, 1): 10, (1, 2): 19, (2, 2): 13, (2, 3): 16,
                  (3, 3): 6, (3, 4): 13, (4, 4): 13}
EXAMPLE_PUBLISHED = {
    "S_11": 10, "TC(1)": 34, "S_12": 19, "TC(2) option 1": 52,
    "c'(3,T_12)": 45, "AC(T_12)": 24.25, "S_22": 13,
    "TC(2) option 2": 67, "c'(3,T_22)": 1, "AC(T_22)": 22.67,
    "Y_4": [1, 1, 1, 0], "TC(4)": 116.2,
}
NOTATION = [
    ("Horizon", "T", "planning horizon"),
    ("Shelf life", "M", "number of age buckets"),
    ("Costs", "a, c, h, p, w", "setup, order, holding, penalty and waste costs"),
]
TABLE2 = {"M": [2, 3, 4], "a": [25, 50, 75], "c": [1, 2], "p": [5, 10, 20]}
TABLE3 = {"Stationary": [8] * 12, "Increasing": list(range(3, 15)),
          "Decreasing": list(range(14, 2, -1)), "Random": [6, 9, 3, 8] * 3}
PATTERN_CODE = {0: "Stationary", 1: "Increasing", 2: "Decreasing", 3: "Random"}
APPENDIX = [(n, (n - 1) % 4, 2 + ((n - 1) // 36) % 3, 25, 1, 10) for n in range(1, 217)]
TABLE4 = {"M": [2, 3, 4], "a": [25, 50, 75], "CV": [0.25, 0.5]}
TABLE6 = []
TABLE7 = []

def instance(n):
    row = APPENDIX[int(n) - 1]
    pattern = PATTERN_CODE[row[1]]
    return dict(T=12, M=row[2], lam=TABLE3[pattern], a=row[3], c=row[4],
                h=1, p=row[5], w=0, dist="poisson", cv=None,
                name=f"Instance {n}", number=n, pattern=pattern)

def instances_table4():
    out = []
    for m in TABLE4["M"]:
        for a in TABLE4["a"]:
            for cv in TABLE4["CV"]:
                out.append(dict(T=12, M=m, lam=[8] * 12, a=a, c=2, h=.5,
                                p=5, w=0, dist="normal", cv=cv,
                                name=f"Normal M={m}, a={a}, CV={cv}",
                                number=len(out) + 1, pattern="Normal"))
    return out

from pathlib import Path
import pandas as pd
import paper_data as P
from heuristic import Heuristic, Instance

out = Path(__file__).parent / "results"
out.mkdir(exist_ok=True)
rows = []
for n in range(1, 217):
    inst = Instance.from_dict(P.instance(n))
    result = Heuristic(inst).step2(Heuristic(inst).step1()["Y"], 100, n)
    rows.append({"instance": n, "TC_H": result["TC"], "cycle_length": result["avg_cycle_length"]})
pd.DataFrame(rows).to_csv(out / "table7_instances.csv", index=False)
pd.DataFrame(P.instances_table4()).to_csv(out / "table6_instances.csv", index=False)
print(f"Wrote {len(rows)} Table 7 instances and {len(P.instances_table4())} Table 6 instances.")

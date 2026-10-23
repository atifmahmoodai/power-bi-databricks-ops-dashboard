#!/usr/bin/env python3
"""Regenerate Databricks-style ops sample CSVs."""
import csv, random
from datetime import datetime, timedelta
from pathlib import Path
random.seed(42)
OUT = Path(__file__).resolve().parents[1] / "data" / "sample"

def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(path.name, len(rows))

plants = [{"PlantId": f"PLT{i}", "PlantName": n, "Region": r}
          for i, (n, r) in enumerate([
              ("North Plant", "North"), ("South Plant", "South"),
              ("East Plant", "East"), ("West Plant", "West")], 1)]
write_csv(OUT/"dim_plant.csv", plants, ["PlantId","PlantName","Region"])

lines = []
for p in plants:
    for ln in range(1, 5):
        lines.append({"LineId": f"{p['PlantId']}-L{ln}", "PlantId": p["PlantId"],
                      "LineName": f"Line {ln}", "CapacityUPH": random.randint(80, 220)})
write_csv(OUT/"dim_line.csv", lines, ["LineId","PlantId","LineName","CapacityUPH"])

shifts = [{"ShiftId": s, "ShiftName": n, "StartHour": h}
          for s, n, h in [("S1","Day",6),("S2","Swing",14),("S3","Night",22)]]
write_csv(OUT/"dim_shift.csv", shifts, ["ShiftId","ShiftName","StartHour"])

ops, dq_flags = [], []
ops_start = datetime(2025, 1, 1)
for d in range(200):
    dt = ops_start + timedelta(days=d)
    for line in lines:
        for shift in shifts:
            if random.random() < 0.02:
                dq_flags.append({"FlagId": f"GAP-{dt.strftime('%Y%m%d')}-{line['LineId']}-{shift['ShiftId']}",
                    "FlagType": "MissingRecord", "ProductionDate": dt.strftime("%Y-%m-%d"),
                    "LineId": line["LineId"], "ShiftId": shift["ShiftId"],
                    "Detail": "No fact row for expected plant/line/shift"})
                continue
            good = random.randint(400, 1600)
            late = 1 if random.random() < 0.04 else 0
            anomaly = 1 if good > line["CapacityUPH"] * 8 * 1.15 else 0
            if late:
                dq_flags.append({"FlagId": f"LATE-{dt.strftime('%Y%m%d')}-{line['LineId']}-{shift['ShiftId']}",
                    "FlagType": "LateArriving", "ProductionDate": dt.strftime("%Y-%m-%d"),
                    "LineId": line["LineId"], "ShiftId": shift["ShiftId"],
                    "Detail": "Record arrived >24h after shift end"})
            if anomaly:
                dq_flags.append({"FlagId": f"ANOM-{dt.strftime('%Y%m%d')}-{line['LineId']}-{shift['ShiftId']}",
                    "FlagType": "AnomalyVolume", "ProductionDate": dt.strftime("%Y-%m-%d"),
                    "LineId": line["LineId"], "ShiftId": shift["ShiftId"],
                    "Detail": f"Output {good} exceeds 115% of theoretical capacity"})
            ops.append({"ProductionId": f"PRD{dt.strftime('%Y%m%d')}{line['LineId']}{shift['ShiftId']}",
                "ProductionDate": dt.strftime("%Y-%m-%d"), "PlantId": line["PlantId"],
                "LineId": line["LineId"], "ShiftId": shift["ShiftId"],
                "UnitsGood": good, "UnitsScrap": random.randint(0, 40),
                "DowntimeMinutes": random.randint(0, 90), "OEE": round(random.uniform(0.55, 0.92), 3),
                "IsLateArriving": late, "IsAnomaly": anomaly})
write_csv(OUT/"fact_production.csv", ops,
    ["ProductionId","ProductionDate","PlantId","LineId","ShiftId","UnitsGood","UnitsScrap","DowntimeMinutes","OEE","IsLateArriving","IsAnomaly"])
write_csv(OUT/"fact_data_quality_flags.csv", dq_flags,
    ["FlagId","FlagType","ProductionDate","LineId","ShiftId","Detail"])
print("Done.")

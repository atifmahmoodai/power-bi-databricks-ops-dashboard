#!/usr/bin/env python3
"""Plant / line / shift ops facts with late-arriving and DQ anomaly flags."""
from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "sample"
SEED = 11
START = date(2024, 1, 1)
END = date(2026, 9, 30)


def date_key(d: date) -> int:
    return int(d.strftime("%Y%m%d"))


def build_dim_date(start: date, end: date) -> pd.DataFrame:
    rows = []
    d = start
    while d <= end:
        rows.append(
            {
                "DateKey": date_key(d),
                "Date": d.isoformat(),
                "Year": d.year,
                "Quarter": f"Q{(d.month - 1) // 3 + 1}",
                "MonthNumber": d.month,
                "MonthName": d.strftime("%B"),
                "MonthShort": d.strftime("%b"),
                "DayOfWeek": d.strftime("%A"),
                "IsWeekend": 1 if d.isoweekday() >= 6 else 0,
            }
        )
        d += timedelta(days=1)
    return pd.DataFrame(rows)


def main() -> None:
    rng = np.random.default_rng(SEED)
    OUT.mkdir(parents=True, exist_ok=True)

    plants = pd.DataFrame(
        [
            {"PlantKey": 1, "PlantId": "PLT-AUS", "PlantName": "Austin Assembly", "Region": "AMER", "Timezone": "America/Chicago"},
            {"PlantKey": 2, "PlantId": "PLT-MEX", "PlantName": "Monterrey Components", "Region": "AMER", "Timezone": "America/Monterrey"},
            {"PlantKey": 3, "PlantId": "PLT-POL", "PlantName": "Wroclaw Precision", "Region": "EMEA", "Timezone": "Europe/Warsaw"},
            {"PlantKey": 4, "PlantId": "PLT-SGP", "PlantName": "Singapore Electronics", "Region": "APAC", "Timezone": "Asia/Singapore"},
            {"PlantKey": 5, "PlantId": "PLT-OH", "PlantName": "Columbus Fabrication", "Region": "AMER", "Timezone": "America/New_York"},
        ]
    )
    shifts = pd.DataFrame(
        [
            {"ShiftKey": 1, "ShiftId": "DAY", "ShiftName": "Day", "StartHour": 6, "EndHour": 14, "ShiftSort": 1},
            {"ShiftKey": 2, "ShiftId": "SWING", "ShiftName": "Swing", "StartHour": 14, "EndHour": 22, "ShiftSort": 2},
            {"ShiftKey": 3, "ShiftId": "NIGHT", "ShiftName": "Night", "StartHour": 22, "EndHour": 6, "ShiftSort": 3},
        ]
    )
    lines = []
    lk = 1
    for _, p in plants.iterrows():
        for n in range(1, int(rng.integers(4, 8))):
            lines.append(
                {
                    "LineKey": lk,
                    "LineId": f"{p.PlantId}-L{n}",
                    "LineName": f"Line {n}",
                    "PlantKey": int(p.PlantKey),
                    "ProductFamily": rng.choice(["Motors", "Controllers", "Harness", "Chassis", "PCB"]),
                    "TargetOEE": round(float(rng.uniform(0.72, 0.88)), 3),
                    "IsActive": 1,
                }
            )
            lk += 1
    dim_line = pd.DataFrame(lines)

    # Production grain: plant-line-shift-date (~3 years * ~5 plants * ~5 lines * 3 shifts * ~260 days)
    prod_rows = []
    dq_rows = []
    pk = 1
    dqk = 1
    d = START
    while d <= END:
        if d.isoweekday() >= 6 and rng.random() < 0.7:
            d += timedelta(days=1)
            continue
        for _, line in dim_line.iterrows():
            for _, sh in shifts.iterrows():
                # occasional missing shift (gap)
                if rng.random() < 0.03:
                    dq_rows.append(
                        {
                            "DQFlagKey": dqk,
                            "PlantKey": int(line.PlantKey),
                            "LineKey": int(line.LineKey),
                            "ShiftKey": int(sh.ShiftKey),
                            "DateKey": date_key(d),
                            "FlagType": "MISSING_SHIFT",
                            "Severity": "High",
                            "FlagDetail": "No production row for expected shift",
                            "DetectedAtUtc": datetime.utcnow().isoformat() + "Z",
                        }
                    )
                    dqk += 1
                    continue

                planned = int(rng.integers(380, 520))
                avail = float(rng.uniform(0.82, 0.99))
                perf = float(rng.uniform(0.78, 1.02))
                qual = float(rng.uniform(0.94, 0.999))
                # inject anomalies
                is_anomaly = 0
                if rng.random() < 0.02:
                    perf = float(rng.uniform(0.35, 0.55))
                    is_anomaly = 1
                good = int(planned * avail * perf * qual)
                scrap = max(0, int(planned * avail * perf * (1 - qual)))
                downtime = round(float(rng.exponential(18)), 1)
                if rng.random() < 0.04:
                    downtime = round(float(rng.uniform(90, 240)), 1)

                # late arriving: recent days sometimes null OEE inputs
                is_late = 0
                if d > END - timedelta(days=3) and rng.random() < 0.25:
                    is_late = 1
                    good = None
                    scrap = None

                oee = None
                if good is not None:
                    oee = round(avail * perf * qual, 4)

                prod_rows.append(
                    {
                        "ProductionKey": pk,
                        "PlantKey": int(line.PlantKey),
                        "LineKey": int(line.LineKey),
                        "ShiftKey": int(sh.ShiftKey),
                        "DateKey": date_key(d),
                        "ProductionDate": d.isoformat(),
                        "PlannedUnits": planned,
                        "GoodUnits": good,
                        "ScrapUnits": scrap,
                        "Availability": round(avail, 4) if not is_late else None,
                        "Performance": round(perf, 4) if not is_late else None,
                        "Quality": round(qual, 4) if not is_late else None,
                        "OEE": oee,
                        "DowntimeMinutes": downtime if not is_late else None,
                        "IsLateArriving": is_late,
                        "IsAnomaly": is_anomaly,
                        "IngestLagHours": int(rng.integers(0, 36)) if is_late else int(rng.integers(0, 4)),
                    }
                )
                pk += 1

                if is_anomaly:
                    dq_rows.append(
                        {
                            "DQFlagKey": dqk,
                            "PlantKey": int(line.PlantKey),
                            "LineKey": int(line.LineKey),
                            "ShiftKey": int(sh.ShiftKey),
                            "DateKey": date_key(d),
                            "FlagType": "OEE_ANOMALY",
                            "Severity": "Medium",
                            "FlagDetail": "Performance below statistical band",
                            "DetectedAtUtc": (datetime.combine(d, datetime.min.time()) + timedelta(hours=6)).isoformat() + "Z",
                        }
                    )
                    dqk += 1
                if is_late:
                    dq_rows.append(
                        {
                            "DQFlagKey": dqk,
                            "PlantKey": int(line.PlantKey),
                            "LineKey": int(line.LineKey),
                            "ShiftKey": int(sh.ShiftKey),
                            "DateKey": date_key(d),
                            "FlagType": "LATE_ARRIVING",
                            "Severity": "Low",
                            "FlagDetail": "Metrics not yet complete",
                            "DetectedAtUtc": datetime.utcnow().isoformat() + "Z",
                        }
                    )
                    dqk += 1
                if scrap is not None and scrap > planned * 0.08:
                    dq_rows.append(
                        {
                            "DQFlagKey": dqk,
                            "PlantKey": int(line.PlantKey),
                            "LineKey": int(line.LineKey),
                            "ShiftKey": int(sh.ShiftKey),
                            "DateKey": date_key(d),
                            "FlagType": "HIGH_SCRAP",
                            "Severity": "High",
                            "FlagDetail": f"Scrap {scrap} vs planned {planned}",
                            "DetectedAtUtc": (datetime.combine(d, datetime.min.time()) + timedelta(hours=8)).isoformat() + "Z",
                        }
                    )
                    dqk += 1
        d += timedelta(days=1)

    # Duplicate detection samples
    if prod_rows:
        sample = prod_rows[100].copy()
        sample["ProductionKey"] = pk
        sample["IsAnomaly"] = 0
        prod_rows.append(sample)
        dq_rows.append(
            {
                "DQFlagKey": dqk,
                "PlantKey": sample["PlantKey"],
                "LineKey": sample["LineKey"],
                "ShiftKey": sample["ShiftKey"],
                "DateKey": sample["DateKey"],
                "FlagType": "DUPLICATE_GRAIN",
                "Severity": "High",
                "FlagDetail": "Duplicate plant-line-shift-date grain",
                "DetectedAtUtc": datetime.utcnow().isoformat() + "Z",
            }
        )

    fact_production = pd.DataFrame(prod_rows)
    fact_dq = pd.DataFrame(dq_rows)
    dim_date = build_dim_date(START, END)

    dim_date.to_csv(OUT / "dim_date.csv", index=False)
    plants.to_csv(OUT / "dim_plant.csv", index=False)
    shifts.to_csv(OUT / "dim_shift.csv", index=False)
    dim_line.to_csv(OUT / "dim_line.csv", index=False)
    fact_production.to_csv(OUT / "fact_production.csv", index=False)
    fact_dq.to_csv(OUT / "fact_data_quality_flags.csv", index=False)

    for p in sorted(OUT.glob("*.csv")):
        print(f"{p.name}: {sum(1 for _ in open(p)) - 1:,}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from pathlib import Path
import sys, pandas as pd
O=Path(__file__).resolve().parents[1]/"data"/"sample"
e=[]; p=pd.read_csv(O/"fact_production.csv"); l=pd.read_csv(O/"dim_line.csv")
if p.ProductionKey.duplicated().sum()>1: e.append("unexpected duplicate ProductionKeys")
if not set(p.LineKey).issubset(set(l.LineKey)): e.append("orphan LineKey")
if len(p)<25000: e.append(f"too small {len(p)}")
if e:
    print("FAIL"); [print("-",x) for x in e]; sys.exit(1)
print(f"OK production={len(p):,} dq={len(pd.read_csv(O/'fact_data_quality_flags.csv')):,}")

# DirectQuery / capacity

| Mode | When |
|------|------|
| Import | Portfolio + plants with daily batch |
| DirectQuery to Databricks SQL WH | Ingest lag < 1h SLA |
| Composite | Dims Import Dual; fact DQ |

Gateway: not required for Databricks cloud SQL; use VNet injection as needed.
Capacity: F64+ if many concurrent DirectQuery visuals; prefer aggregations (Plant×Day) for exec page.

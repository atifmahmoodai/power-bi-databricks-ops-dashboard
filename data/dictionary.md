# Data dictionary — plant operations + data quality

| Table | Grain | Rows | Notes |
|-------|-------|------|-------|
| dim_date | Day | ~1k | |
| dim_plant | Plant | 5 | Region + timezone |
| dim_line | Production line | 20 | TargetOEE |
| dim_shift | Shift | 3 | Sort by ShiftSort |
| fact_production | Plant×Line×Shift×Date | **~47k** | Late-arriving nulls, anomaly flags |
| fact_data_quality_flags | One flag event | **~2.5k** | MISSING_SHIFT, LATE_ARRIVING, OEE_ANOMALY, HIGH_SCRAP, DUPLICATE_GRAIN |

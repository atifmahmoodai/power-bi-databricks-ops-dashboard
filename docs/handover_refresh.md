# Handover & refresh / performance

## Import demo refresh

Replace CSVs → Refresh in Desktop → Publish. Keep dataset **under ~100 MB** for snappy shared capacity demos.

## DirectQuery production

1. Point queries at Databricks SQL warehouse views.  
2. Schedule nothing on the dataset (query-on-open); optionally use aggregations tables.  
3. Monitor warehouse cost + Power BI query duration in metrics app.

## Data quality page checklist

- [ ] MissingRecord count explained (calendar of expected shifts)  
- [ ] LateArriving investigated with pipeline SLA  
- [ ] AnomalyVolume reviewed with process engineering  

## Filters to preserve

Date · Plant · Line · Shift — sync slicers across Ops and DQ pages.

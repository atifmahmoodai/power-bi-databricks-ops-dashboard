# Relationships

| From | To | Cardinality |
|------|----|-------------|
| dim_line[PlantId] | dim_plant[PlantId] | Many:1 |
| fact_production[PlantId] | dim_plant[PlantId] | Many:1 |
| fact_production[LineId] | dim_line[LineId] | Many:1 |
| fact_production[ShiftId] | dim_shift[ShiftId] | Many:1 |

For flags, create a **weak** link via LineId + ShiftId + ProductionDate (composite key column recommended):

`DQKey = ProductionDate & "|" & LineId & "|" & ShiftId` on both facts.

### Performance notes

- Import demo is well under **100 MB**.  
- For DirectQuery: avoid `SUMX` over large unrelated tables; prefer simple aggregates.  
- Pre-aggregate gold tables in Databricks for executive dashboards.  
- Disable Auto date/time; use a proper date dimension if you extend the model.

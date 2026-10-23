| From | To | Card | Active |
|------|----|------|--------|
| fact_production[PlantKey] | dim_plant[PlantKey] | *∶1 | Y |
| fact_production[LineKey] | dim_line[LineKey] | *∶1 | Y |
| fact_production[ShiftKey] | dim_shift[ShiftKey] | *∶1 | Y |
| fact_production[DateKey] | dim_date[DateKey] | *∶1 | Y |
| fact_data_quality_flags[LineKey] | dim_line[LineKey] | *∶1 | Y |
| fact_data_quality_flags[DateKey] | dim_date[DateKey] | *∶1 | Y |
| dim_line[PlantKey] | dim_plant[PlantKey] | *∶1 | Y |
Single direction only.

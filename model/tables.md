# Model tables — ops

## dim_plant
PlantId, PlantName, Region. Grain: plant.

## dim_line
LineId, PlantId, LineName, CapacityUPH. Grain: production line.

## dim_shift
ShiftId (S1/S2/S3), ShiftName, StartHour.

## fact_production (grain: Date × Line × Shift)

UnitsGood, UnitsScrap, DowntimeMinutes, OEE, IsLateArriving, IsAnomaly.

## fact_data_quality_flags (grain: one quality event)

FlagType: MissingRecord | LateArriving | AnomalyVolume.  
Used for the Data Quality page; may not 1:1 join every production row (gaps have no fact).

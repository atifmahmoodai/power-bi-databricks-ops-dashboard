// fact_production typing + DQKey
let
    Source = Csv.Document(File.Contents("data/sample/fact_production.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"ProductionId", type text}, {"ProductionDate", type date},
        {"PlantId", type text}, {"LineId", type text}, {"ShiftId", type text},
        {"UnitsGood", Int64.Type}, {"UnitsScrap", Int64.Type},
        {"DowntimeMinutes", Int64.Type}, {"OEE", type number},
        {"IsLateArriving", Int64.Type}, {"IsAnomaly", Int64.Type}
    }),
    AddKey = Table.AddColumn(Typed, "DQKey",
        each Text.From([ProductionDate]) & "|" & [LineId] & "|" & [ShiftId], type text)
in
    AddKey

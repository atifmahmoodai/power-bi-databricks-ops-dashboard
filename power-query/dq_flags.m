// Data quality flags
let
    Source = Csv.Document(File.Contents("data/sample/fact_data_quality_flags.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"FlagId", type text}, {"FlagType", type text}, {"ProductionDate", type date},
        {"LineId", type text}, {"ShiftId", type text}, {"Detail", type text}
    }),
    AddKey = Table.AddColumn(Typed, "DQKey",
        each Text.From([ProductionDate]) & "|" & [LineId] & "|" & [ShiftId], type text)
in
    AddKey

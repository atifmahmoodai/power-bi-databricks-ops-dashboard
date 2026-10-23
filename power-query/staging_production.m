let
    Source = Csv.Document(File.Contents(pSourcePath & "/fact_production.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
    Promote = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Promote,{
        {"ProductionKey",Int64.Type},{"PlantKey",Int64.Type},{"LineKey",Int64.Type},{"ShiftKey",Int64.Type},
        {"DateKey",Int64.Type},{"OEE",type number},{"IsLateArriving",Int64.Type},{"IsAnomaly",Int64.Type},{"IngestLagHours",Int64.Type}}),
    IsLateFlag = Table.AddColumn(Typed,"IsLate",each [IsLateArriving]=1, type logical),
    RowHash = Table.AddColumn(IsLateFlag,"RowHash",each Text.From([ProductionKey]) & "-" & Text.From([DateKey]), type text)
in RowHash // Load OFF

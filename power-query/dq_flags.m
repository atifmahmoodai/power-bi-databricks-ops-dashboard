let
    Source = Csv.Document(File.Contents(pSourcePath & "/fact_data_quality_flags.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
    Promote = Table.PromoteHeaders(Source,[PromoteAllScalars=true])
in Promote

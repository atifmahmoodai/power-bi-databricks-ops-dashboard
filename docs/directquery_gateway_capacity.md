# DirectQuery, gateway, capacity
- Databricks SQL Warehouse: Serverless preferred for BI spikes
- Gateway: only if hybrid on-prem sources joined
- Start F32/F64; watch DirectQuery latency in Fabric metrics
- Push aggregates to gold tables; keep PBIX visuals thin

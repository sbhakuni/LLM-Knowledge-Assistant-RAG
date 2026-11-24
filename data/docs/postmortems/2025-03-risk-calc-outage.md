# 2025-03 Risk Calc Outage

## Summary
The risk calculation service returned `ERR_RISK_504` for 40 minutes during the morning batch run.

## Root cause
`ExposureBatchJob` leaked database connections. The Oracle pool (`HikariPool-1`) reached its maximum of 20 connections, so new requests timed out.

## Resolution
The service was restarted, and the leak was fixed in `ExposureBatchJob` by closing connections in a `finally` block.

## Action items
- Add an alert when pool utilization is above 80%.
- Add a test that checks the batch job releases its connections.

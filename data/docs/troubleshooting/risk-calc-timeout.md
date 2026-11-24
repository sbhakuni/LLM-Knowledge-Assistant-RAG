# Risk Calculation Timeout

## Symptom
The risk calculation service returns `ERR_RISK_504: upstream timeout`, or requests hang and then fail.

## Likely causes
1. The Pricing API is slow or unavailable.
2. The Oracle connection pool is exhausted. The logs show `HikariPool-1 - Connection is not available, request timed out`.

## Checks
1. Check the Pricing API health dashboard.
2. Count active connections on RISK_DB. If they equal `hikari.maximum-pool-size`, the pool is exhausted.
3. Check whether a batch job is running, because `ExposureBatchJob` holds connections for a long time.

## Fix
- If the Pricing API is down, wait for it to recover and then restart the service.
- If the pool is exhausted, restart the service and look for a connection leak. Raise `hikari.maximum-pool-size` only after ruling out a leak.

See the postmortem 2025-03 Risk Calc Outage for a past incident with this error.

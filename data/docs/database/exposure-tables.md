# Exposure Tables (RISK_DB)

## CPTY_EXPOSURE_DAILY
Daily counterparty exposure. One row per counterparty, per netting set, per day.

Columns: `CPTY_ID`, `AS_OF_DATE`, `NETTING_SET_ID`, `PFE`, `EPE`.

This is the table to query for counterparty exposure data.

## TRADE_POSITION
Open trade positions. Join to `CPTY_EXPOSURE_DAILY` on `CPTY_ID`.

Columns: `TRADE_ID`, `CPTY_ID`, `NOTIONAL`, `CURRENCY`, `MATURITY_DATE`.

## Access
Use the read replica for reporting queries. Never run heavy queries on the primary.

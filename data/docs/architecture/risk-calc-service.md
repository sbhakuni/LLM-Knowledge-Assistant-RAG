# Risk Calculation Service

## Overview
Spring Boot service that computes counterparty exposure (PFE and EPE). It reads trades from the Oracle database RISK_DB, fetches market data from the Pricing API, and publishes results to the Kafka topic `risk.exposure.v1`.

## Dependencies
- Oracle RISK_DB (read replica), accessed through a HikariCP connection pool.
- Pricing API (REST). The client timeout is 30 seconds.
- Kafka cluster, topic `risk.exposure.v1`.

## Configuration
- `hikari.maximum-pool-size`: default 20.
- `pricing.client.timeout-seconds`: default 30.
- Health endpoint: `/actuator/health`.

## Environments
| Environment | URL |
|---|---|
| QA | https://risk-calc.qa.internal.example |
| Prod | https://risk-calc.internal.example |

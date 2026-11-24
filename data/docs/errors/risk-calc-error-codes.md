# Risk Calculation Service Error Codes

## ERR_RISK_504
Upstream timeout. The service did not get a response from the Pricing API or the database within the timeout. See the troubleshooting guide "Risk Calculation Timeout".

## ERR_RISK_400
Invalid request. The `asOfDate` parameter is missing or not in `YYYY-MM-DD` format.

## ERR_RISK_404
Counterparty not found. The `cptyId` does not exist in the table `CPTY_EXPOSURE_DAILY`.

## ERR_RISK_503
Kafka publish failed. Check the Kafka cluster status and the topic `risk.exposure.v1`.

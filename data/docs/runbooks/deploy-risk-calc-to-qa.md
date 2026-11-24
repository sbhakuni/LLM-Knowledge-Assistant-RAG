# Deploy Risk Calculation Service to QA

## Prerequisites
- Your pull request is merged to the `develop` branch.
- The build on `develop` is green.

## Steps
1. Open Jenkins and run the job `risk-calc/deploy-qa`.
2. Set the parameter `BUILD_NUMBER` to the build you want to deploy.
3. Wait for the stage `Smoke Test` to pass.
4. Verify that `https://risk-calc.qa.internal.example/actuator/health` returns `UP`.

## Rollback
Re-run `risk-calc/deploy-qa` with the previous `BUILD_NUMBER`.

## Deploying to Prod
Prod deployments need an approved change ticket. Use the job `risk-calc/deploy-prod`, and run it outside the 09:00-17:00 trading window.

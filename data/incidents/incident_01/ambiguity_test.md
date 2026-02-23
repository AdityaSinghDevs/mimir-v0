## RUN 1

*H1:* Upstream Service Timeout Cascade (55%)
*H2:* DB Auth Failure Breaking Config/Routing (30%)
*H3:* Credential Rotation / Secret Expiry for config_svc (15%)

## RUN 2

*H1:* DB Authentication Failure Causing Upstream Dependency Timeouts (55%)
*H2:* Upstream Service Overload / Capacity Exhaustion Causing Gateway Timeouts (30%)
*H3:* Config Refresh Race Condition Causing Partial/Inconsistent Routing State (15%)

## RUN 3

*H1* Downstream dependency timeout cascading through gateway (55%)
*H2:* Config service partial/failed reload destabilizing worker-3 (30%)
*H3:* DB proxy auth failure blocking config-dependent request paths (15%)


## Ambiguity: HIGH
### Empirical validation: 3-run hypothesis instability observed.

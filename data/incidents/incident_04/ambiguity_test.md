## RUN 1
H1: Primary DB node crash / network partition (65%)
H2: Application connection pool lag (25%)
H3: Replication lag at promotion (10%)

## RUN 2
H1: Primary failure → automated failover (66%)
H2: DNS / pool refresh delay (24%)
H3: Replica lag at promotion (10%)

## RUN 3
H1: dc1 primary became unreachable, orchestrator failover triggered (64%)
H2: Client-side routing delay extended outage (26%)
H3: Minor replication delay at switchover (10%)

## Ambiguity: LOW

### Empirical Validation:
- Dominant hypothesis stable across runs (~64–66%).
- All competing hypotheses are secondary and explanatory, not structurally independent.
- No log lines indicate replication corruption, split-brain, or data divergence.
- Failure narrative is linear and infra-driven.
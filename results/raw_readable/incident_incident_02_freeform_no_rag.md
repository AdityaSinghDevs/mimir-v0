# Incident: incident_02

## Title
Missing data with lost modifications across repositories

## Ground Truth Root Cause
Accidental deletion of primary production DB instead of replica by an engineer during manual replication recovery.

---

## Run 1

Root Cause :
The PostgreSQL primary server is experiencing issues that prevent data replication and API writes, leading to data loss and write failures.

Supporting Evidence :
- `2026-02-22T10:03:18.907Z WARN postgres-primary-0 {"timestamp":"2026-02-22T10:03:18.907Z","level":"WARN","component":"wal","msg":"replication slot lag exceeds threshold","slot":"replica_slot_1","write_lag_bytes":184732921}`
- `2026-02-22T10:04:16.402Z WARN postgres-primary-0 {"timestamp":"2026-02-22T10:04:16.402Z","level":"WARN","component":"checkpointer","msg":"checkpoint taking longer than expected","duration_ms":74231}`
- `2026-02-22T10:04:29.119Z ERROR postgres-replica-1 {"timestamp":"2026-02-22T10:04:29.119Z","level":"ERROR","component":"recovery","msg":"invalid timeline history reference","timeline":4}`

## Run 2

Root Cause :
The root cause of the issue is a data inconsistency due to a failed base backup operation that resulted in the PostgreSQL replica being out of sync with the primary, leading to subsequent write failures.

Supporting Evidence :
- `2026-02-22T10:03:31.556Z ERROR pg-backup-agent-7c4b9d6f8c-lp7sx {"level":"ERROR","ts":"2026-02-22T10:03:31.556Z","msg":"base backup failed","error":"connection reset during COPY","attempt":3}`
- `2026-02-22T10:04:29.119Z ERROR postgres-replica-1 {"timestamp":"2026-02-22T10:04:29.119Z","level":"ERROR","component":"recovery","msg":"invalid timeline history reference","timeline":4}`
- `2026-02-22T10:04:41.763Z WARN  bg-reconciler-6d7f8c9b4e-rt5h2 {"level":"WARN","ts":"2026-02-22T10:04:41.763Z","msg":"detected partial user state during reconciliation","user_id":"u_483291","missing_fields":["profile","preferences"]}`

## Run 3

Root Cause :
PostgreSQL primary replica is experiencing severe replication issues, causing data lags and serialization failures, which result in API service write failures and timeouts.

Supporting Evidence :
- Log entry "replication slot lag exceeds threshold" on 2026-02-22T10:03:18.907Z indicates persistent replication lag.
- Error "connection reset during COPY" in 2026-02-22T10:03:31.556Z shows that the base backup attempt failed due to connection issues.
- Log "invalid timeline history reference" on 2026-02-22T10:04:29.119Z reveals that there's an issue with timeline history, possibly due to a split-brain scenario or inconsistent replication.
- "detected partial user state during reconciliation" in 2026-02-22T10:04:41.763Z suggests that the PostgreSQL instance is unable to reconcile the state of users, leading to missing data.
- "primary connectivity change observed" in 2026-02-22T10:04:55.508Z indicates that the replication topology has changed, likely due to a failure of the primary node, further complicating synchronization.
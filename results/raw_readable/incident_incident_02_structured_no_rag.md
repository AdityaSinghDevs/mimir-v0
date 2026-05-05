# Incident: incident_02

## Title
Missing data with lost modifications across repositories

## Ground Truth Root Cause
Accidental deletion of primary production DB instead of replica by an engineer during manual replication recovery.

---

## Run 1

**Symptom Identification:**
Users experience data loss, missing modifications, and errors when accessing repositories, particularly with write operations to the database failing. Additionally, there are signs of replication lag and issues with the PostgreSQL replica.

**Hypothesis Generation:**
1. **Replication Lag Leading to Data Loss:** The high replication lag could result in data being lost due to incomplete data transfer between nodes.
2. **Write Failures Caused by Replication Lag:** The serialization failure and write timeouts might be caused by ongoing replication lag.
3. **PostgreSQL Replica Errors Due to Missing Data:** The errors like "invalid timeline history reference" suggest that the replica is not synchronized correctly, leading to data corruption.

**Verification Checks:**
1. **Replication Lag Leading to Data Loss:**
- **Log Evidence Contradicting Hypothesis:** There's no direct log indicating immediate data loss; however, the persistent replication lag (e.g., `replication slot lag exceeds threshold`) suggests ongoing issues.
- **Log Evidence Supporting Hypothesis:** High replication lag (`replication slot lag exceeds threshold`) indicates potential data gaps and delays in updates, which can lead to data loss or inconsistencies.
2. **Write Failures Caused by Replication Lag:**
- **Log Evidence Contradicting Hypothesis:** No explicit mention of write failures directly caused by replication lag.
- **Log Evidence Supporting Hypothesis:** Multiple instances of write timeouts and serialization failures (`write request received` followed by `write failed`), occurring at various stages, suggest that the issue is related to the write process being blocked by replication lag.
3. **PostgreSQL Replica Errors Due to Missing Data:**
- **Log Evidence Contradicting Hypothesis:** Log lines do not explicitly state that data loss is due to missing data on the replica.
- **Log Evidence Supporting Hypothesis:** The `invalid timeline history reference` error occurs, implying that the replica does not have the necessary timeline information, which could be due to replication lag or other synchronization issues.

**Root Cause Conclusion:**
The most likely root cause is **Replication Lag Leading to Data Loss**. Persistent replication lag is causing both data loss and write failures due to serialization issues.

**Supporting Evidence:**
- **High Replication Lag:** 
  ```
  2026-02-22T10:03:18.907Z WARN  postgres-primary-0 {"timestamp":"2026-02-22T10:03:18.907Z","level":"WARN","component":"wal","msg":"replication slot lag exceeds threshold","slot":"replica_slot_1","write_lag_bytes":184732921}
  ```
- **Write Failures:**
  ```
  2026-02-22T10:04:02.881Z ERROR api-writesvc-6f9c8d7b5f-q2m8k {"level":"ERROR","ts":"2026-02-22T10:04:02.881Z","msg":"write failed","request_id":"req-9c2b1e7a","error":"serialization failure","status":500}
  ```
  ```
  2026-02-22T10:04:16.402Z WARN  postgres-primary-0 {"timestamp":"2026-02-22T10:04:16.402Z","level":"WARN","component":"checkpointer","msg":"checkpoint taking longer than expected","duration_ms":74231}
  ```

## Run 2

Symptom Identification:
Users experience issues accessing repositories and losing data and modifications. There are also API service write failures, data replication lags, and API write timeouts.

Hypothesis Generation:
1. Data replication lag causing API write failures.
2. API write failures leading to serialization failures.
3. PostgreSQL primary server experiencing issues affecting both data replication and API writes.

Verification Checks:
1. **Data Replication Lag Leading to API Write Failures**:
- Log "replication slot lag exceeds threshold" indicates a replication lag issue on the PostgreSQL primary node.
- Log "write failed" due to "serialization failure" suggests an underlying issue in the PostgreSQL cluster that might be exacerbated by the replication lag.
2. **API Write Failures Causing Serialization Failures**:
- Multiple log entries for API write failures (e.g., "write request received", "write failed") indicate that these failures could be causing serialization issues.
3. **PostgreSQL Primary Server Issues Affecting Both Data Replication and API Writes**:
- Log "checkpoint taking longer than expected" shows a PostgreSQL primary server issue.
- Log "invalid timeline history reference" and "partial user state detected" indicate PostgreSQL issues impacting the state synchronization and replication process.

Root Cause Conclusion:
The PostgreSQL primary server issues are the most likely root cause, as they affect both data replication and API writes, leading to data replication lags and API write failures.

Supporting Evidence:
1. `2026-02-22T10:03:18.907Z WARN postgres-primary-0 {"timestamp":"2026-02-22T10:03:18.907Z","level":"WARN","component":"wal","msg":"replication slot lag exceeds threshold","slot":"replica_slot_1","write_lag_bytes":184732921}`
2. `2026-02-22T10:04:16.402Z WARN postgres-primary-0 {"timestamp":"2026-02-22T10:04:16.402Z","level":"WARN","component":"checkpointer","msg":"checkpoint taking longer than expected","duration_ms":74231}`
3. `2026-02-22T10:04:29.119Z ERROR postgres-replica-1 {"timestamp":"2026-02-22T10:04:29.119Z","level":"ERROR","component":"recovery","msg":"invalid timeline history reference","timeline":4}`
4. `2026-02-22T10:04:41.763Z WARN bg-reconciler-6d7f8c9b4e-rt5h2 {"level":"WARN","ts":"2026-02-22T10:04:41.763Z","msg":"detected partial user state during reconciliation","user_id":"u_483291","missing_fields":["profile","preferences"]}`

## Run 3

**Symptom Identification:**
- Users experience missing data and lost modifications in repositories.
- There are errors in accessing repositories.
- The incident started at 10:04 UTC.
- Monitoring alerts indicate data replication lags and API service write failures.

**Hypothesis Generation:**
1. **Data Replication Failure:** PostgreSQL replica is unable to catch up with the primary, causing data inconsistencies and writes failing.
2. **Write Service Error:** API write requests are timing out or failing due to underlying issues like serialization failures or connection resets.
3. **Reconciliation Errors:** Reconciliation process is failing due to missing fields, leading to inconsistent states of users' profiles and preferences.

**Verification Checks:**
1. **Data Replication Failure:**
- Log evidence: `replication slot lag exceeds threshold` (2026-02-22T10:03:18.907Z), `base backup failed` (2026-02-22T10:03:31.556Z), `invalid timeline history reference` (2026-02-22T10:04:29.119Z), `partial user state during reconciliation` (2026-02-22T10:04:41.763Z).
- This indicates replication is not stable, leading to data inconsistencies and write failures.
2. **Write Service Error:**
- Log evidence: `write request received` (2026-02-22T10:03:11.482Z), `write failed` (2026-02-22T10:04:02.881Z), `serialization failure` (2026-02-22T10:04:02.881Z), `context deadline exceeded` (2026-02-22T10:05:02.936Z).
- This suggests write requests are failing due to internal service issues, possibly related to serialization problems or timeouts.
3. **Reconciliation Errors:**
- Log evidence: `detected partial user state during reconciliation` (2026-02-22T10:04:41.763Z), `invalid timeline history reference` (2026-02-22T10:04:29.119Z).
- These errors indicate the reconciliation process is having difficulty, leading to missing data and inconsistent user states.

**Root Cause Conclusion:**
The most likely root cause is **Data Replication Failure** due to unstable replication between the primary and replica PostgreSQL instances, which leads to data inconsistencies and write failures.

**Supporting Evidence:**
- `replication slot lag exceeds threshold` (2026-02-22T10:03:18.907Z)
- `base backup failed` (2026-02-22T10:03:31.556Z)
- `invalid timeline history reference` (2026-02-22T10:04:29.119Z)
- `partial user state during reconciliation` (2026-02-22T10:04:41.763Z)
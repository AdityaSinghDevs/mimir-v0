# Incident: incident_03

## Title
Missing data with lost modifications across repositories(Same as 02, increased ambiguity_level)

## Ground Truth Root Cause
Primary cluster reinitialized against incorrect or empty data directory during replication recovery procdeure

---

## Run 1

Symptom Identification:
Users are experiencing write failures, data missing, and lost modifications. The API service is also reporting write failures.

Hypothesis Generation:
1. PostgreSQL primary node went down due to unexpected relation inventory mismatch causing data loss.
2. There's a conflict in the replica-handshake metadata between primary and replica nodes leading to write failures.
3. Replication lags have caused API service write failures.

Verification Checks:
1. **PostgreSQL Primary Node Failure Hypothesis:**
- Log Evidence: 
- `2026-02-22T10:03:52.004Z WARN postgres-primary-6f9c8d7c4b-k2m7p {"component":"catalog","msg":"unexpected relation inventory size","expected_relations":5,"observed_relations":1}`
- `2026-02-22T10:03:47.881Z INFO postgres-primary-6f9c8d7c4b-k2m7p {"component":"startup","msg":"database instance starting after recovery attempt","timeline":1}`
   This suggests a restart of the PostgreSQL primary node, likely due to an unexpected state, which may be indicative of a failure.
2. **Metadata Mismatch Hypothesis:**
- Log Evidence:
- `2026-02-22T10:04:49.233Z WARN repl-orchestrator-6d4b7f8c9d-m0p2 {"component":"orchestrator","msg":"leadership uncertainty","reason":"conflicting primary reports","observed_nodes":2}`
- `2026-02-22T10:04:33.512Z WARN postgres-primary-6f9c8d7c4b-k2m7p {"component":"replication","msg":"replica handshake metadata mismatch","peer":"replica","local_epoch":"42","peer_epoch":"41"`
   This indicates conflicting reports from the primary and replica nodes regarding their epochs, suggesting a problem in the metadata synchronization.
3. **Replication Lag and API Service Write Failures:**
- Log Evidence:
- `2026-02-22T10:03:19.907Z WARN postgres-replica-5c7d9f6b8f-r8q4n {"component":"postgres","role":"replica","msg":"replication lag above threshold","slot":"replica_slot_1","write_lag_ms":18432,"flush_lag_ms":17601}`
- `2026-02-22T10:04:06.845Z ERROR user-api-7f6c9d8b5c-v3n4m {"level":"ERROR","msg":"write request failed","request_id":"a9e3c1f2","error":"serialization failure","status":500}`
- `2026-02-22T10:04:21.090Z WARN worker-reconcile-6c8d7f9b4a-q2w8e {"level":"WARN","msg":"partial reconciliation detected","job":"user-sync","missing_entities":12,"request_id":"bg-44f1"`
   High replication lags and API service write failures suggest the lag is significant enough to impact write operations.

Root Cause Conclusion:
The most likely root cause is the unexpected relation inventory mismatch in the PostgreSQL primary node causing data loss, which led to a restart. This restart caused conflicts in the replica-handshake metadata, further disrupting the replication process and resulting in API service write failures.

Supporting Evidence:
- Unexpected relation inventory size (2026-02-22T10:03:52.004Z).
- Metadata mismatch warning (2026-02-22T10:04:33.512Z).
- Data loss during restart (2026-02-22T10:03:47.881Z).

## Run 2

**Symptom Identification:**
Users report missing data, write failures, lost modifications, and errors in accessing repositories. The issue started around 10:04 UTC, marked by API service write failures and data replication lags.

**Hypothesis Generation:**
1. **Data Replication Failure:** The database may have encountered an error during the replication process leading to missing data.
2. **Primary Replica Mismatch:** There might be a mismatch between the primary and replica instances causing write failures.
3. **Recovery Errors:** Post-recovery issues could lead to unexpected behavior, such as relation state mismatches and serialization failures.

**Verification Checks:**
1. **Data Replication Failure:**
- Log: `2026-02-22T10:03:44.910Z INFO postgres-primary-6f9c8d7c4b-k2m7p {"component":"recovery","msg":"attempting replication state reset","mode":"manual_recovery"}` - Indicates a manual recovery attempt due to replication lag or other issues.
- Log: `2026-02-22T10:03:52.004Z WARN postgres-primary-6f9c8d7c4b-k2m7p {"component":"catalog","msg":"unexpected relation inventory size","expected_relations":5,"observed_relations":1}` - Suggests an unexpected reduction in relations, which could imply data loss or corruption during replication.
2. **Primary Replica Mismatch:**
- Log: `2026-02-22T10:04:49.233Z WARN repl-orchestrator-6d4b7f8c9d-m0p2 {"component":"orchestrator","msg":"leadership uncertainty","reason":"conflicting primary reports","observed_nodes":2}` - Shows conflicting primary reports indicating instability.
- Log: `2026-02-22T10:04:33.512Z WARN postgres-primary-6f9c8d7c4b-k2m7p {"component":"replication","msg":"replica handshake metadata mismatch","peer":"replica","local_epoch":"42","peer_epoch":"41"}` - Confirms a metadata mismatch between primary and replica.
3. **Recovery Errors:**
- Log: `2026-02-22T10:03:44.910Z INFO postgres-primary-6f9c8d7c4b-k2m7p {"component":"recovery","msg":"attempting replication state reset","mode":"manual_recovery"}` - Manual recovery is triggered, suggesting an unstable state.
- Log: `2026-02-22T10:05:07.406Z INFO postgres-replica-5c7d9f6b8f-r8q4n {"component":"postgres","role":"replica","msg":"recovery paused awaiting WAL","last_received_lsn":"0/69FF2A0"}` - Recovery pause indicates a problem with the last received LSN.

**Root Cause Conclusion:**
The root cause appears to be a data replication failure leading to a mismatch between primary and replica instances, causing leadership uncertainty and manual recovery attempts.

**Supporting Evidence:**
- Log: `2026-02-22T10:03:44.910Z INFO postgres-primary-6f9c8d7c4b-k2m7p {"component":"recovery","msg":"attempting replication state reset","mode":"manual_recovery"}` confirms manual recovery due to replication issues.
- Log: `2026-02-22T10:04:33.512Z WARN postgres-primary-6f9c8d7c4b-k2m7p {"component":"replication","msg":"replica handshake metadata mismatch","peer":"replica","local_epoch":"42","peer_epoch":"41"}` indicates a significant metadata mismatch.
- Log: `2026-02-22T10:04:49.233Z WARN repl-orchestrator-6d4b7f8c9d-m0p2 {"component":"orchestrator","msg":"leadership uncertainty","reason":"conflicting primary reports","observed_nodes":2}` confirms conflicting primary reports.

## Run 3

**Symptom Identification:**
Users experience missing data, write failures, lost modifications, and errors in accessing repositories. This is indicated by various errors such as serialization failure, relation state mismatch, and write request failures.

**Hypothesis Generation:**
1. **Database Replication Lag:** The system is experiencing significant replication lag which could lead to data inconsistencies and write failures.
2. **Replica Metadata Mismatch:** The replica might be out of sync due to a metadata discrepancy.
3. **API Service Issues:** The API service might be failing due to underlying database issues, causing write failures.

**Verification Checks:**
1. **Database Replication Lag:**
- Log: `2026-02-22T10:03:19.907Z WARN postgres-replica-5c7d9f6b8f-r8q4n {"component":"postgres","role":"replica","msg":"replication lag above threshold","slot":"replica_slot_1","write_lag_ms":18432,"flush_lag_ms":17601}`
- Log: `2026-02-22T10:03:52.004Z WARN postgres-primary-6f9c8d7c4b-k2m7p {"component":"catalog","msg":"unexpected relation inventory size","expected_relations":5,"observed_relations":1}`
- Log: `2026-02-22T10:04:33.512Z WARN postgres-primary-6f9c8d7c4b-k2m7p {"component":"replication","msg":"replica handshake metadata mismatch","peer":"replica","local_epoch":"42","peer_epoch":"41"}`
   These logs suggest that the replica is behind the primary, leading to unexpected behavior and write failures.
2. **Replica Metadata Mismatch:**
- Log: `2026-02-22T10:04:33.512Z WARN postgres-primary-6f9c8d7c4b-k2m7p {"component":"replication","msg":"replica handshake metadata mismatch","peer":"replica","local_epoch":"42","peer_epoch":"41"}`
- Log: `2026-02-22T10:04:58.771Z ERROR user-api-7f6c9d8b5c-v3n4m {"level":"ERROR","msg":"write request failed","request_id":"b71d8a90","error":"relation state mismatch","status":500}`
   These logs indicate that there's a mismatch between the local and peer epochs, which could lead to metadata discrepancies and subsequent write failures.
3. **API Service Issues:**
- Log: `2026-02-22T10:04:06.845Z ERROR user-api-7f6c9d8b5c-v3n4m {"level":"ERROR","msg":"write request failed","request_id":"a9e3c1f2","error":"serialization failure","status":500}`
- Log: `2026-02-22T10:04:21.090Z WARN worker-reconcile-6c8d7f9b4a-q2w8e {"level":"WARN","msg":"partial reconciliation detected","job":"user-sync","missing_entities":12,"request_id":"bg-44f1"`
   While these logs point to API service failures, they do not directly link to database replication issues.

**Root Cause Conclusion:**
The most likely root cause is that the database replication lag has caused the replica to be out of sync, leading to unexpected behavior and write failures.

**Supporting Evidence:**
- Log: `2026-02-22T10:03:19.907Z WARN postgres-replica-5c7d9f6b8f-r8q4n {"component":"postgres","role":"replica","msg":"replication lag above threshold","slot":"replica_slot_1","write_lag_ms":18432,"flush_lag_ms":17601}`
- Log: `2026-02-22T10:04:33.512Z WARN postgres-primary-6f9c8d7c4b-k2m7p {"component":"replication","msg":"replica handshake metadata mismatch","peer":"replica","local
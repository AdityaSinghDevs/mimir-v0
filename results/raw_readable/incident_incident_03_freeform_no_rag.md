# Incident: incident_03

## Title
Missing data with lost modifications across repositories(Same as 02, increased ambiguity_level)

## Ground Truth Root Cause
Primary cluster reinitialized against incorrect or empty data directory during replication recovery procdeure

---

## Run 1

Root Cause :
The root cause of the issue is an unexpected loss of data during a replication process, leading to inconsistent states and subsequent failures across various services.

Supporting Evidence :
- `2026-02-22T10:04:06.845Z ERROR user-api-7f6c9d8b5c-v3n4m {"level":"ERROR","msg":"write request failed","request_id":"a9e3c1f2","error":"serialization failure","status":500}` indicates that a write request failed due to serialization failure, suggesting issues with data consistency.
- `2026-02-22T10:04:49.233Z WARN repl-orchestrator-6d4b7f8c9d-m0p2 {"component":"orchestrator","msg":"leadership uncertainty","reason":"conflicting primary reports","observed_nodes":2}` indicates leadership uncertainty, which can lead to inconsistent data states and service failures.
- `2026-02-22T10:04:33.512Z WARN postgres-primary-6f9c8d7c4b-k2m7p {"component":"replication","msg":"replica handshake metadata mismatch","peer":"replica","local_epoch":"42","peer_epoch":"41"}` shows a metadata mismatch between the replica and the primary, further indicating problems with data consistency and replication.
- `2026-02-22T10:03:58.301Z WARN postgres-replica-5c7d9f6b8f-r8q4n {"component":"postgres","role":"replica","msg":"requested timeline 7 not found in history file","current_timeline":6}` suggests that the replica does not have the correct timeline information, possibly due to a data loss or corruption during the replication process.

## Run 2

Root Cause :
The PostgreSQL replica is experiencing a timeline mismatch during its initial recovery process, leading to serialization failures and lost data.

Supporting Evidence (explicit log lines or events) :
- 2026-02-22T10:04:49.233Z WARN repl-orchestrator-6d4b7f8c9d-m0p2 {"component":"orchestrator","msg":"leadership uncertainty","reason":"conflicting primary reports","observed_nodes":2}
- 2026-02-22T10:04:58.771Z ERROR user-api-7f6c9d8b5c-v3n4m {"level":"ERROR","msg":"write request failed","request_id":"b71d8a90","error":"relation state mismatch","status":500}
- 2026-02-22T10:04:58.771Z ERROR user-api-7f6c9d8b5c-v3n4m {"level":"ERROR","msg":"write request failed","request_id":"b71d8a90","error":"relation state mismatch","status":500}

## Run 3

Root Cause :
The PostgreSQL primary and replica are experiencing issues with replication, causing a loss of data and write failures.

Supporting Evidence :
- Multiple logs indicate high replication lag, including "replication lag above threshold" (2026-02-22T10:03:19.907Z WARN postgres-replica-5c7d9f6b8f-r8q4n).
- Base backup failed (2026-02-22T10:03:27.114Z ERROR backup-agent-7bbf9d6f55-x1z9c), leading to manual recovery attempts.
- Relation inventory size discrepancy and timeline mismatch (2026-02-22T10:03:52.004Z WARN postgres-primary-6f9c8d7c4b-k2m7p, 2026-02-22T10:04:49.233Z WARN repl-orchestrator-6d4b7f8c9d-m0p2).
- Mismatched replica handshake metadata and leadership uncertainty (2026-02-22T10:04:33.512Z WARN postgres-primary-6f9c8d7c4b-k2m7p, 2026-02-22T10:04:49.233Z WARN repl-orchestrator-6d4b7f8c9d-m0p2).
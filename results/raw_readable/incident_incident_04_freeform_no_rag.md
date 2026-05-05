# Incident: incident_04

## Title
Out-of-date information due to network divergence

## Ground Truth Root Cause
Automated failover via Orchestrator (Raft consensus) triggered due to ~40s network partition between network hub and primary data center, leading to cross-region promotion of MySQL and divergent writes between data centers.

---

## Run 1

Root Cause :
The primary MySQL database node lost leadership due to a failure, causing a split-brain scenario where two replicas became primary. The API service was unable to connect to the now-failed primary database, leading to write latency issues and eventually connection refusal errors.

Supporting Evidence (explicit log lines or events):
- `2026-03-12T20:02:46.772Z orchestrator-6f9c7b5d8c-kx2pl INFO failover: promoting candidate=dc2-mysql-replica-1 reason=lost quorum with dc1-mysql-primary`
- `2026-03-12T20:02:44.331Z orchestrator-6f9c7b5d8c-kx2pl WARN raft: heartbeat timeout from leader=dc1-mysql-primary last_contact_ms=40123`
- `2026-03-12T20:02:52.614Z api-service-7d9f6c8f5b-l2m9q {"level":"WARN","ts":"2026-03-12T20:02:52.614Z","msg":"write latency high","dependency":"mysql","latency_ms":1834,"request_id":"req-3ac8d2f1"}`
- `2026-03-12T20:03:21.332Z api-service-7d9f6c8f5b-l2m9q {"level":"ERROR","ts":"2026-03-12T20:03:21.332Z","msg":"db connection error","error":"connection refused","request_id":"req-a82d1c3e"}`
- `2026-03-12T20:03:07.451Z webhook-worker-5f8c9d7bb6-qt9vn {"level":"ERROR","ts":"2026-03-12T20:03:07.451Z","msg":"delivery attempt failed","event":"order.created","retry":2,"error":"dial tcp 10.0.1.12:3306: connect: connection refused"}`
- `2026-03-12T20:03:36.114Z api-service-7d9f6c8f5b-l2m9q {"level":"INFO","ts":"2026-03-12T20:03:36.114Z","msg":"connection pool refreshed","dependency":"mysql"}`

## Run 2

Root Cause :
The primary MySQL node became unavailable, leading to a failover to a replica node. This resulted in a loss of connectivity for the application due to the connection refusal errors and high write latency issues.

Supporting Evidence :
- `2026-03-12T20:02:39.904Z mysql-replica-0-6c8dbf9f7d-hj4rt [Warning] Slave I/O: error reconnecting to master 'repl@dc1-mysql-primary:3306' - retry-time: 60 retries: 1, Error_code: 2003`
- `2026-03-12T20:02:44.331Z orchestrator-6f9c7b5d8c-kx2pl WARN raft: heartbeat timeout from leader=dc1-mysql-primary last_contact_ms=40123`
- `2026-03-12T20:02:45.019Z orchestrator-6f9c7b5d8c-kx2pl INFO raft: initiating leader election term=483`
- `2026-03-12T20:02:48.203Z mysql-dc2-replica-1-5b7fd9c6f9-rp8zm [Note] role transition: REPLICA -> PRIMARY`
- `2026-03-12T20:03:07.451Z webhook-worker-5f8c9d7bb6-qt9vn {"level":"ERROR","ts":"2026-03-12T20:03:07.451Z","msg":"delivery attempt failed","event":"order.created","retry":2,"error":"dial tcp 10.0.1.12:3306: connect: connection refused"}`
- `2026-03-12T20:03:21.332Z api-service-7d9f6c8f5b-l2m9q {"level":"ERROR","ts":"2026-03-12T20:03:21.332Z","msg":"db connection error","error":"connection refused","request_id":"req-a82d1c3e"}`

## Run 3

Root Cause :
The primary MySQL node experienced a failure, causing a failover to its replica, which was then disconnected from the primary after a short time. This led to a loss of quorum and a subsequent promotion of the replica to the primary role.

Supporting Evidence :
- `2026-03-12T20:02:46.772Z orchestrator-6f9c7b5d8c-kx2pl INFO failover: promoting candidate=dc2-mysql-replica-1 reason=lost quorum with dc1-mysql-primary`
- `2026-03-12T20:02:52.614Z api-service-7d9f6c8f5b-l2m9q {"level":"WARN","ts":"2026-03-12T20:02:52.614Z","msg":"write latency high","dependency":"mysql","latency_ms":1834,"request_id":"req-3ac8d2f1"}`
- `2026-03-12T20:03:07.451Z webhook-worker-5f8c9d7bb6-qt9vn {"level":"ERROR","ts":"2026-03-12T20:03:07.451Z","msg":"delivery attempt failed","event":"order.created","retry":2,"error":"dial tcp 10.0.1.12:3306: connect: connection refused"}`
- `2026-03-12T20:03:21.332Z api-service-7d9f6c8f5b-l2m9q {"level":"ERROR","ts":"2026-03-12T20:03:21.332Z","msg":"db connection error","error":"connection refused","request_id":"req-a82d1c3e"}`
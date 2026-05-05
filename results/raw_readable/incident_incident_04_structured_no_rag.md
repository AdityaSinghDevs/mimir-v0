# Incident: incident_04

## Title
Out-of-date information due to network divergence

## Ground Truth Root Cause
Automated failover via Orchestrator (Raft consensus) triggered due to ~40s network partition between network hub and primary data center, leading to cross-region promotion of MySQL and divergent writes between data centers.

---

## Run 1

**Symptom Identification:** 
Users report outdated information, missing pages, and stale data. Monitoring alerts show primary database node health check failures, increased write latency, and timeouts.

**Hypothesis Generation:**
1. **Primary MySQL Node Failure:** The primary MySQL node is experiencing issues causing service disruptions.
2. **Replica Node Replication Lag:** The replica nodes may be lagging behind the primary, leading to data inconsistency.
3. **Network Connectivity Issues:** There might be network connectivity problems between nodes affecting data retrieval and updates.

**Verification Checks:**
1. **Primary MySQL Node Failure:**
- Log evidence: `2026-03-12T20:02:39.904Z mysql-replica-0-6c8dbf9f7d-hj4rt [Warning] Slave I/O: error reconnecting to master 'repl@dc1-mysql-primary:3306' - retry-time: 60 retries: 1, Error_code: 2003`. This indicates an issue with connecting to the primary node, possibly due to failure.
2. **Replica Node Replication Lag:**
- Log evidence: `2026-03-12T20:02:45.019Z orchestrator-6f9c7b5d8c-kx2pl INFO raft: initiating leader election term=483`. This shows a leader election process initiated after the primary node experienced issues, suggesting potential replication lag.
3. **Network Connectivity Issues:**
- Log evidence: `2026-03-12T20:03:21.332Z api-service-7d9f6c8f5b-l2m9q {"level":"ERROR","ts":"2026-03-12T20:03:21.332Z","msg":"db connection error","error":"connection refused","request_id":"req-a82d1c3e"}`. This error suggests a connection refusal, indicating network connectivity issues.

**Root Cause Conclusion:**
The most likely root cause is **Primary MySQL Node Failure**. This conclusion is supported by the warning about failing to reconnect to the primary node, which indicates a primary node issue leading to service disruptions.

**Supporting Evidence:**
- `2026-03-12T20:02:39.904Z mysql-replica-0-6c8dbf9f7d-hj4rt [Warning] Slave I/O: error reconnecting to master 'repl@dc1-mysql-primary:3306' - retry-time: 60 retries: 1, Error_code: 2003`
- `2026-03-12T20:02:45.019Z orchestrator-6f9c7b5d8c-kx2pl INFO raft: initiating leader election term=483`

## Run 2

**Symptom Identification:**
Users are experiencing outdated information, missing pages, and stale data. The incident started at 20:02 UTC. Monitoring alerts indicate primary database node health check failures, increased write latency, and timeouts.

**Hypothesis Generation:**
1. **Primary Database Node Failure:** The primary MySQL node may have experienced an unexpected failure or restart.
2. **Replication Lag and Disruption:** There might be an issue with the replication lag, causing inconsistencies or inability to access the primary database node.
3. **Network Connectivity Issues:** The network connection between nodes could be disrupted, preventing clients from accessing the updated database state.

**Verification Checks:**
1. **Primary Database Node Failure:**
- Log line "2026-03-12T20:02:39.904Z mysql-replica-0-6c8dbf9f7d-hj4rt [Warning] Slave I/O: error reconnecting to master 'repl@dc1-mysql-primary:3306' - retry-time: 60 retries: 1" suggests a failure in connecting to the primary node.
- Log line "2026-03-12T20:02:44.331Z orchestrator-6f9c7b5d8c-kx2pl WARN raft: heartbeat timeout from leader=dc1-mysql-primary last_contact_ms=40123" indicates a heartbeat timeout from the leader node, possibly signaling a failure.
2. **Replication Lag and Disruption:**
- Log line "2026-03-12T20:02:44.331Z orchestrator-6f9c7b5d8c-kx2pl WARN raft: heartbeat timeout from leader=dc1-mysql-primary last_contact_ms=40123" shows a heartbeat timeout, which is indicative of a disruption in the replication process.
- Log line "2026-03-12T20:02:52.614Z api-service-7d9f6c8f5b-l2m9q {"level":"WARN","ts":"2026-03-12T20:02:52.614Z","msg":"write latency high","dependency":"mysql","latency_ms":1834,"request_id":"req-3ac8d2f1"}" indicates high write latency, which could be due to replication lag or primary node unavailability.
3. **Network Connectivity Issues:**
- Log line "2026-03-12T20:03:07.451Z webhook-worker-5f8c9d7bb6-qt9vn {"level":"ERROR","ts":"2026-03-12T20:03:07.451Z","msg":"delivery attempt failed","event":"order.created","retry":2,"error":"dial tcp 10.0.1.12:3306: connect: connection refused"}" shows a connection refusal, suggesting issues with network connectivity.
- Log line "2026-03-12T20:03:21.332Z api-service-7d9f6c8f5b-l2m9q {"level":"ERROR","ts":"2026-03-12T20:03:21.332Z","msg":"db connection error","error":"connection refused","request_id":"req-a82d1c3e"}" confirms that connections are being refused, further indicating network connectivity problems.

**Root Cause Conclusion:**
The primary hypothesis that aligns best with the observed symptoms is that the primary MySQL node experienced a failure, leading to a disruption in replication and network connectivity.

**Supporting Evidence:**
- Log line "2026-03-12T20:02:39.904Z mysql-replica-0-6c8dbf9f7d-hj4rt [Warning] Slave I/O: error reconnecting to master 'repl@dc1-mysql-primary:3306' - retry-time: 60 retries: 1" indicates a failure in reconnecting to the primary node.
- Log line "2026-03-12T20:02:44.331Z orchestrator-6f9c7b5d8c-kx2pl WARN raft: heartbeat timeout from

## Run 3

**Symptom Identification:**  
Users report outdated information, missing pages, and stale data. This is indicated by an increase in write latency and timeouts, as well as a failure of the primary database node's health checks.

**Hypothesis Generation:**  
1. **Primary Database Node Failure:** The primary database node may have failed and been taken over by another replica, leading to the observed issues.
2. **Replica Connection Refusal:** The replicas might be refusing connections due to some internal issue.
3. **Network Latency Issues:** High network latency could be causing delays in communication between nodes, resulting in the observed symptoms.

**Verification Checks:**  
1. **Primary Database Node Failure:**
- Log Evidence: 
     ```
     2026-03-12T20:02:46.772Z orchestrator-6f9c7b5d8c-kx2pl INFO failover: promoting candidate=dc2-mysql-replica-1 reason=lost quorum with dc1-mysql-primary
     ```
   This log suggests the primary node lost its leadership and was replaced by a replica, which explains the observed symptom.
2. **Replica Connection Refusal:**
- Log Evidence:
     ```
     2026-03-12T20:02:52.614Z api-service-7d9f6c8f5b-l2m9q {"level":"WARN","ts":"2026-03-12T20:02:52.614Z","msg":"write latency high","dependency":"mysql","latency_ms":1834,"request_id":"req-3ac8d2f1"}
     2026-03-12T20:03:21.332Z api-service-7d9f6c8f5b-l2m9q {"level":"ERROR","ts":"2026-03-12T20:03:21.332Z","msg":"db connection error","error":"connection refused","request_id":"req-a82d1c3e"}
     ```
   These logs indicate that connections to the replicas are being refused, which can lead to write failures and delayed data updates.
3. **Network Latency Issues:**
- Log Evidence:
     None directly shows network latency issues; however, the frequent connection refusals and increased write latency suggest possible network-related problems.

**Root Cause Conclusion:**  
The most likely root cause is the primary database node failure, leading to a new replica taking over, and subsequent connection refusal issues on the old primary replica.

**Supporting Evidence:**  
- Primary node failure log:
  ```
  2026-03-12T20:02:46.772Z orchestrator-6f9c7b5d8c-kx2pl INFO failover: promoting candidate=dc2-mysql-replica-1 reason=lost quorum with dc1-mysql-primary
  ```
- Connection refusal logs:
  ```
  2026-03-12T20:02:52.614Z api-service-7d9f6c8f5b-l2m9q {"level":"WARN","ts":"2026-03-12T20:02:52.614Z","msg":"write latency high","dependency":"mysql","latency_ms":1834,"request_id":"req-3ac8d2f1"}
  2026-03-12T20:03:21.332Z api-service-7d9f6c8f5b-l2m9q {"level":"ERROR","ts":"2026-03-12T20:03:21.332Z","msg":"db connection error","error":"connection refused","request_id":"req-a82d1c3e"}
  ```
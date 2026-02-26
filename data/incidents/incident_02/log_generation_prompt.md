Now, you are generating synthetic system logs for a research study on LLM-based incident diagnosis.

Your task is NOT to make the root cause obvious.

You must produce realistic, ambiguous logs that reflect the following fixed causal structure:

Root cause:
Accidental deletion of primary production database instead of replica during manual replication recovery.

Precursors:
1. Elevated DB load
2. Replication lag between primary and secondary database
3. Attempt to remove specific user-related data
4. Ongoing maintenance on replication topology
5. Repeated pg_basebackup failure prior to manual intervention

Competing plausible hypotheses:
H2: Corrupted replica / failover misconfiguration
H3: Replication lag due to load spikes

Affected components:
- API services
- Database cluster (primary + replica)
- Background workers
- Backup agent
- Replication/orchestrator processes

Observable constraints:
Visible logs may include:
- DB replication state transitions
- WAL/slot lag metrics
- Timeline changes
- Base backup attempts
- Replica recovery state
- Orchestrator leadership/failover messages
- API write failures
- Worker reconciliation errors

Not visible:
- Direct shell commands
- Human mistakes
- Explicit DROP statements
- Slack messages
- Manual intervention logs
- Explicit DB query text
- Ingress/config-layer logs

Observable service-level signals:
- Elevated 5xx on write operations
- Missing or inconsistent user data
- Replication lag alerts
- API write failures
- Background reconciliation detecting partial data

Time window:
~10:03–10:05 UTC

Ambiguity Level: MODERATE

Ambiguity Requirements (Very Important):

- Evidence must support at least two competing hypotheses.
- Root cause must be slightly better supported than alternatives.
- No single log line may conclusively prove deletion.
- At least one log line should indicate an unexpected cluster state discontinuity (e.g., sudden invalid timeline reference, missing WAL history, abrupt primary unavailability, unexpected role transition).
- The discontinuity must be explainable by both failover misconfiguration and sudden primary loss.
- Avoid symmetric evidence that perfectly balances all hypotheses — root cause should have marginally stronger structural coherence.

Generation Requirements:

- Do NOT explicitly state deletion.
- Do NOT use phrases like “DROP DATABASE”, “database removed”, “admin command”, “misconfiguration detected”.
- Avoid dramatic or narrative phrasing.
- Avoid explicit human intent.
- Include subtle overlap between replication failure and data inconsistency.
- Include mild operational noise.
- Keep logs between 10–14 lines.
- Do NOT include recovery steps.
- Only generate logs inside the failure window.
- Ensure timestamps progress realistically.

Output only raw log lines.
Do not explain anything.
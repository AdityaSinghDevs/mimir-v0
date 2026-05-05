# Incident: incident_01

## Title
Elevated 5xx errors across edge services

## Ground Truth Root Cause
DB permission change caused invalid config artifact generation, leading to partial config application and upstream routing failures.

---

## Run 1

**Symptom Identification:** 
Users experience elevated 5xx errors when accessing customer sites. Specifically, there is an increase in 504 Gateway Timeout errors at the ingress level and 502 Bad Gateway errors at the gateway API level, indicating degraded service performance.

**Hypothesis Generation:**
1. **Network Latency Issues:** The network might be experiencing high latency, causing timeouts.
2. **Service Outage:** There may have been a temporary outage of one or more services.
3. **Configuration Update Failures:** A configuration update could have failed, leading to service unavailability.

**Verification Checks:**
1. **Network Latency Issues:**
- Log evidence: Multiple instances show a 504 error, which indicates a timeout issue between the client and the upstream server.
     ```
     2026-02-22T14:21:03.112Z ingress-nginx-7c9f8d6c5b-qx2lm controller INFO 10.24.6.18 - - [22/Feb/2026:14:21:03 +0000] "GET / HTTP/1.1" 504 0 "-" "Mozilla/5.0" request_id=3f2c1a8d upstream_response_time=5.002
     2026-02-22T14:21:04.087Z ingress-nginx-7c9f8d6c5b-qx2lm controller WARN upstream timed out (110: Connection timed out) while reading response header from upstream, request_id=3f2c1a8d
     ```
2. **Service Outage:**
- Log evidence: There are no consistent logs indicating a complete shutdown or failure of any service, but there is a spike in 5xx errors that correlate with the start time of the incident.
     ```
     2026-02-22T14:21:03.112Z ingress-nginx-7c9f8d6c5b-qx2lm controller INFO 10.24.6.18 - - [22/Feb/2026:14:21:03 +0000] "GET / HTTP/1.1" 504 0 "-" "Mozilla/5.0" request_id=3f2c1a8d upstream_response_time=5.002
     ```
3. **Configuration Update Failures:**
- Log evidence: There are multiple warnings about partial configuration application and delays in the next refresh schedule, suggesting a failure in the process.
     ```
     2026-02-22T14:21:07.981Z config-service-5b7d9c6f44-hk8s3 stdout {"ts":"2026-02-22T14:21:07.981Z","level":"WARN","component":"config-parser","msg":"partial config applied","artifact_bytes":184320,"node":"worker-3"}
     2026-02-22T14:21:08.204Z config-service-5b7d9c6f44-hk8s3 stdout {"ts":"2026-02-22T14:21:08.204Z","level":"INFO","component":"scheduler","msg":"next refresh scheduled","interval_sec":300}
     ```

**Root Cause Conclusion:**
The most likely root cause is a failure in the configuration update process, which led to partial configuration application and subsequent delays, resulting in service degradation and increased 5xx errors.

**Supporting Evidence:**
- Multiple logs show a partial configuration application (`partial config applied`), which occurred during the incident timeframe.
- Logs indicate a delay in the next refresh schedule (`next refresh scheduled`, `interval_sec`: 300), further supporting the idea that the configuration update did not proceed as expected.

## Run 2

**Symptom Identification:**
Elevated 5xx errors reported by users when accessing customer sites, accompanied by service degradation and timeouts observed across edge services.

**Hypothesis Generation:**
1. **Timeouts due to network issues:** Gateway API is experiencing long delays, causing timeouts and subsequent 502 responses.
2. **Service restart or misconfiguration:** The configuration service may have restarted improperly, leading to partial updates and delayed application deployments.
3. **Resource exhaustion on edge services:** High load on edge services might be causing them to timeout requests.

**Verification Checks:**
1. **Timeouts due to network issues:**
- Log evidence: Multiple entries show gateway API responding with 502 status codes and noting "timeout contacting dependency" and "upstream timed out (110: Connection timed out)."
- Support: 
     ```
     2026-02-22T14:21:11.404Z gateway-api-6f4b9d7c8d-mp9k2 stdout {"ts":"2026-02-22T14:21:11.404Z","level":"INFO","component":"health","msg":"health check passed","duration_ms":12}
     2026-02-22T14:21:12.267Z gateway-api-6f4b9d7c8d-mp9k2 stdout {"ts":"2026-02-22T14:21:12.266Z","level":"ERROR","component":"http-client","msg":"timeout contacting dependency","request_id":"c0e9f1aa","timeout_ms":5000}
     ```
2. **Service restart or misconfiguration:**
- Log evidence: Configuration service shows partial config applied and next refresh scheduled after a restart, but no apparent immediate impact.
- Support:
     ```
     2026-02-22T14:21:07.981Z config-service-5b7d9c6f44-hk8s3 stdout {"ts":"2026-02-22T14:21:07.981Z","level":"WARN","component":"config-parser","msg":"partial config applied","artifact_bytes":184320,"node":"worker-3"}
     2026-02-22T14:21:08.204Z config-service-5b7d9c6f44-hk8s3 stdout {"ts":"2026-02-22T14:21:08.204Z","level":"INFO","component":"scheduler","msg":"next refresh scheduled","interval_sec":300}
     ```
3. **Resource exhaustion on edge services:**
- No clear evidence of resource exhaustion; high 5xx errors are not correlated with high CPU usage or memory usage in edge services.
- Support:
     ```
     2026-02-22T14:21:03.112Z ingress-nginx-7c9f8d6c5b-qx2lm controller INFO 10.24.6.18 - - [22/Feb/2026:14:21:03 +0000] "GET / HTTP/1.1" 504 0 "-" "Mozilla/5.0" request_id=3f2c1a8d upstream_response_time=5.002
     2026-02-22T14:21:05.441Z gateway-api-6f4b9d7c8d-mp9k2 stdout {"ts":"2026-02-22T14:21:05.440Z","level":"ERROR","component":"http-server","msg":"request failed","request_id":"3f2c1a8d","status":502,"latency_ms":4876}
     ```

**Root Cause Conclusion:**
The most likely root cause is network timeouts due to slow response times of upstream services. This is evidenced by multiple instances where gateway API reports timeouts and requests fail with 502 status codes.

**Supporting Evidence:**
- Multiple 502 and 504 errors with upstream timeouts noted.
- Gateway API's health checks passing intermittently but failing with timeout errors.

## Run 3

**Symptom Identification:**
Users experience elevated 5xx errors, particularly 504 Gateway Timeout and 502 Bad Gateway errors, which degrade service availability on customer sites. The issue started around 14:21 UTC.

**Hypothesis Generation:**
1. **Increased load on the backend services**: The influx of requests could be overwhelming the backend services, leading to increased timeouts.
2. **Configuration issues causing health checks to fail**: Changes in configuration might be causing health checks to fail, leading to service degradations.
3. **Network connectivity issues affecting backend access**: Network connectivity problems could prevent backend services from responding, resulting in timeout errors.

**Verification Checks:**
1. **Increased load on the backend services:**
- Log evidence: Multiple instances show upstream timeouts and bad gateway responses (`504` and `502`), suggesting that backend services may be the bottleneck.
- Verification: Confirm if backend services were indeed under heavy load during the incident period.
2. **Configuration issues causing health checks to fail:**
- Log evidence: There is a warning about partial config application and a refresh schedule, indicating potential configuration issues.
- Verification: Check if the configuration loader triggered a refresh and whether the partial config application indicates an issue that might have affected the health checks.
3. **Network connectivity issues affecting backend access:**
- Log evidence: A denied connection error (`DENIED`) in the database proxy indicates potential network connectivity issues.
- Verification: Investigate the network traffic patterns and ensure there are no network-related disruptions.

**Root Cause Conclusion:**
The most likely root cause is an increased load on the backend services, as evidenced by the high frequency of `504` and `502` errors. The observed warnings about partial config application and health checks being affected suggest configuration issues but less directly impact the symptom of degraded services compared to the overwhelming load on backend services.

**Supporting Evidence:**
- Multiple instances showing `504` and `502` errors, e.g., 
  ```
  2026-02-22T14:21:03.112Z ingress-nginx-7c9f8d6c5b-qx2lm controller INFO 10.24.6.18 - - [22/Feb/2026:14:21:03 +0000] "GET / HTTP/1.1" 504 0 "-" "Mozilla/5.0" request_id=3f2c1a8d upstream_response_time=5.002
  ```
- Warning about health check failure, e.g.,
  ```
  2026-02-22T14:21:12.267Z gateway-api-6f4b9d7c8d-mp9k2 stdout {"ts":"2026-02-22T14:21:12.266Z","level":"ERROR","component":"http-client","msg":"timeout contacting dependency","request_id":"c0e9f1aa","timeout_ms":5000}
  ```
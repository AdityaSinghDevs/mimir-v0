# Incident: incident_01

## Title
Elevated 5xx errors across edge services

## Ground Truth Root Cause
DB permission change caused invalid config artifact generation, leading to partial config application and upstream routing failures.

---

## Run 1

Root Cause :
The root cause of the issue is a connectivity problem between the edge services and the backend services, which is causing high 5xx errors and degraded performance.

Supporting Evidence :
1. Log entry at 2026-02-22T14:21:03.112Z shows an initial 504 error indicating a timeout while trying to reach the upstream service from the ingress-nginx controller.
2. The following logs at 2026-02-22T14:21:04.087Z and 2026-02-22T14:21:05.441Z show warnings and errors related to timeouts while the upstream service is being accessed by the ingress-nginx controller.
3. At 2026-02-22T14:21:12.266Z, there's a log entry showing an error where a timeout occurs while contacting a dependent service.
4. Logs also show that the configuration service has refreshed its configuration and restarted, which could lead to temporary issues with service availability, as evidenced by the 502 status code at 2026-02-22T14:21:10.118Z for a GET request to assets/app.js.

## Run 2

Root Cause :
The most likely root cause is a timeout issue affecting the communication between the Gateway API and its dependencies, specifically the health check and the request processing.

Supporting Evidence :
- 2026-02-22T14:21:12.267Z gateway-api-6f4b9d7c8d-mp9k2 stdout {"ts":"2026-02-22T14:21:12.266Z","level":"ERROR","component":"http-client","msg":"timeout contacting dependency","request_id":"c0e9f1aa","timeout_ms":5000}
- 2026-02-22T14:21:13.913Z ingress-nginx-7c9f8d6c5b-qx2lm controller WARN 10.24.6.18 - - [22/Feb/2026:14:21:13 +0000] "GET /login HTTP/1.1" 502 0 "-" "Mozilla/5.0" request_id=c0e9f1aa upstream_response_time=5.000

## Run 3

Root Cause :
Gateway API service is experiencing timeouts due to health checks failing, leading to 502 Bad Gateway responses.

Supporting Evidence (explicit log lines or events) :
1. 2026-02-22T14:21:12.266Z gateway-api-6f4b9d7c8d-mp9k2 stdout {"ts":"2026-02-22T14:21:12.266Z","level":"ERROR","component":"http-client","msg":"timeout contacting dependency","request_id":"c0e9f1aa","timeout_ms":5000}
2. 2026-02-22T14:21:13.913Z ingress-nginx-7c9f8d6c5b-qx2lm controller WARN 10.24.6.18 - - [22/Feb/2026:14:21:13 +0000] "GET /login HTTP/1.1" 502 0 "-" "Mozilla/5.0" request_id=c0e9f1aa upstream_response_time=5.000
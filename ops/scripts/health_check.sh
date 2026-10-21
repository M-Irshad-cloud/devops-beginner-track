#!/usr/bin/env bash
# Health check for the services in this stack.
# Exit code: 0 = all healthy, 1 = at least one unhealthy.

TIMEOUT=3
RETRIES=2

# name|url|expected_http_status
CHECKS=(
  "app|http://app:5000/health|200"
  "nginx-proxy|http://nginx/health|200"
  "prometheus|http://prometheus:9090/-/healthy|200"
  "grafana|http://grafana:3000/api/health|200"
)

failed=0

for entry in "${CHECKS[@]}"; do
  IFS='|' read -r name url expected <<< "$entry"
  code="000"
  secs="0"
  for attempt in $(seq 1 "$RETRIES"); do
    read -r code secs < <(curl -s -o /dev/null -w '%{http_code} %{time_total}' --max-time "$TIMEOUT" "$url")
    code=${code:-000}
    [ "$code" = "$expected" ] && break
    sleep 1
  done

  if [ "$code" = "$expected" ]; then
    echo "$(date '+%F %T') OK   $name ($url) http=$code time=${secs}s"
  else
    echo "$(date '+%F %T') FAIL $name ($url) http=$code expected=$expected after $RETRIES attempts"
    failed=$((failed + 1))
  fi
done

if [ "$failed" -gt 0 ]; then
  echo "$(date '+%F %T') SUMMARY $failed service(s) unhealthy"
  exit 1
fi
echo "$(date '+%F %T') SUMMARY all services healthy"

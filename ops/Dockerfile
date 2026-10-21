FROM ubuntu:24.04
RUN apt-get update \
 && apt-get install -y --no-install-recommends cron curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /ops
COPY scripts/ /ops/scripts/
COPY crontab /etc/ops-crontab
RUN sed -i 's/\r$//' /ops/scripts/*.sh /etc/ops-crontab \
 && chmod +x /ops/scripts/*.sh \
 && crontab /etc/ops-crontab
CMD ["cron", "-f"]

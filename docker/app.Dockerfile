FROM python:3.9

WORKDIR /app

RUN apt-get update -qq \
  && DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -qqq cron \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY . .
COPY docker/entrypoint.sh /app/entrypoint.sh
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/app/entrypoint.sh"]

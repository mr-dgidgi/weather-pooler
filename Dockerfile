FROM python:3.14.0a2-alpine3.20

RUN <<EOF
pip3 install influxdb-client
pip3 install configparser
pip3 install requests
pip3 install pyyaml
echo "*/5 * * * * root cd /etc/weather-pooler/; python3 weather-pooler.py" > /ect/cron.d/weather-pooler
EOF

CMD ["mkdir", "-m", "755","/etc/weather-pooler/"]

WORKDIR /etc/weather-pooler
COPY weather-pooler.py weather-pooler.py
COPY station.yml station.yml
COPY config.ini config.ini

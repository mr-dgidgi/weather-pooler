FROM python:3.14.0a2-alpine3.20

RUN <<EOF
pip3 install influxdb-client
pip3 install configparser
pip3 install requests
pip3 install pyyaml
mkdir", "-m", "755","/etc/weather-pooler/
EOF

WORKDIR /etc/weather-pooler
COPY weather-pooler.py weather-pooler.py

CMD ["python3 weather-pooler.py"]
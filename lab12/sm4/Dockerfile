FROM python:3.8-alpine

RUN apk update && apk add gcc g++ make openssl-dev python3-dev libffi-dev autoconf

WORKDIR /opt/ctf
RUN mkdir -p /opt/ctf

COPY server.py .
COPY func.py .
COPY sm4.py .

EXPOSE 23367
CMD ["python", "-u", "server.py"]
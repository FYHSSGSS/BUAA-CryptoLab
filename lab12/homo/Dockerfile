FROM python:3.8-alpine

RUN apk update && apk add gcc g++ make openssl-dev python3-dev libffi-dev autoconf

WORKDIR /opt/ctf
RUN mkdir -p /opt/ctf

COPY homoserver.py .
COPY poly.py .

EXPOSE 22338
CMD ["python", "-u", "homoserver.py"]
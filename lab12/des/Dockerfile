FROM python:3.8-alpine

RUN apk update && apk add gcc g++ make openssl-dev python3-dev libffi-dev autoconf

WORKDIR /opt/ctf
RUN mkdir -p /opt/ctf

COPY desserver.py .

RUN pip install pycryptodome

EXPOSE 22336
CMD ["python", "-u", "desserver.py"]
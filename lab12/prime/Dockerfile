FROM python:3.8-alpine

RUN apk update && apk add gcc g++ make openssl-dev python3-dev libffi-dev autoconf

WORKDIR /opt/ctf
RUN mkdir -p /opt/ctf

COPY primeserver.py .

EXPOSE 22354
CMD ["python", "-u", "primeserver.py"]
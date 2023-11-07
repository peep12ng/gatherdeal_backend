FROM python:3.11

WORKDIR /backend

ADD . .

RUN python3 -m pip install -U pip
RUN pip install -r requirements.txt

CMD ["/bin/bash", "/backend/docker-entrypoint.sh"]
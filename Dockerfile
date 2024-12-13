FROM python:3.12-slim-bullseye

LABEL org.opencontainer.image.source=https://github.com/olexiyn/image-gen

WORKDIR /wheels
ADD ./requirements.txt /wheels

WORKDIR /opt
RUN apt update && python3 -m venv venv && . venv/bin/activate && pip install --upgrade pip && \
        pip install -r /wheels/requirements.txt -f /wheels && \
        rm -rf /wheels && \
        rm -rf /root/.cache/pip/*

COPY app/ /opt/app
COPY templates/ /opt/templates

ADD server.py /opt
ADD start.sh /opt

RUN chmod 755 /opt/start.sh

EXPOSE 8080
CMD ["/opt/start.sh"]
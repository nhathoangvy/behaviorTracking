FROM python:3.6-slim
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install gcc mono-mcs && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /behavior

ADD . /behavior

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

ENV NAME behavior

CMD python3 manage.py runserver 0.0.0.0:8000

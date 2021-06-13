FROM python:3.6-slim

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential \
    && apt-get -y install default-libmysqlclient-dev \
    && apt-get -y install mariadb-client

COPY ./clarity /clarity/clarity
COPY uwsgi.ini /clarity
WORKDIR /clarity
RUN pip3 install -r clarity/requirements.txt

COPY nginx.conf /etc/nginx

EXPOSE 80

COPY start.sh /clarity
COPY generate_database.py /clarity
RUN chmod +x ./start.sh
ENTRYPOINT ["./start.sh"]

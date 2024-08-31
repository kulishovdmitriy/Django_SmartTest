FROM python:3.10

RUN apt-get update
RUN apt-get install git

RUN mkdir /srv/project
WORKDIR /srv

COPY ./src ./project
COPY ./requirements.txt ./
COPY ./run_server.sh ./

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x ./run_server.sh

CMD ["./run_server.sh"]
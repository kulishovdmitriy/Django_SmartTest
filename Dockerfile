FROM python:3.10

RUN apt-get update
RUN apt-get install git

WORKDIR /srv

COPY ./src ./
COPY requirements.txt ./
COPY ./run_server.sh ./

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["./run_server.sh"]
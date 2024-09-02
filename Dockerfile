FROM python:3.10

RUN apt-get update && apt-get install -y git

RUN mkdir -p /project/src
WORKDIR /project/src

COPY ./src ./

WORKDIR /project
COPY ./requirements.txt ./
COPY ./commands ./

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

WORKDIR /project/src

CMD ["bash"]
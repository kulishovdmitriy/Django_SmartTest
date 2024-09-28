# Application Smart Test

### Annex for various tests

## Install app

The following steps for deploying the application:

    1. git clone https://github.com/kulishovdmitriy/Django_SmartTest

If you want to launch a local application without Docker/Docker-Compose, you need to create a virtual environment (commands for Linux)

If you want to start from docker-compose, miss these steps

    python3 -m venv venv
    source ./venv/bin/activate

Re -check the correctness of the location python:

    which python

Set addictions from requirements.txt

    pip install -r requirements.txt

install docker:

    sudo apt update
    sudo apt install apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt update
    sudo apt install docker-ce -y
    sudo systemctl status docker
    sudo usermod -aG docker ${USER}
    newgrp docker
    docker --version

Install docker-compose:

    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    docker-compose --version

Create a file `.env` as described in the example `.env.example` and fill in your values

In file `.env` you can switch between `dev`, `staging` or `prod`:

Important!! When `RUN_MODE=dev` django uses `sqlite` database!!! You need to make containers in docker-compose, except 
`backend` 

    RUN_MODE=

Follow the starting command for `docker-compose`

    2. docker compose up -- build

In the container `postgres`,follow the command to create a new user.
Here `psql` - is a customer utility for PostgreSQL, and `-U postgres` indicates that you are in as a super - user Postgressql `postgres`.
Replace `your_database` and `new_user`. 

    docker compose exec postgres psql -U postgres
    
    CREATE USER new_user WITH PASSWORD 'password123'

    ALTER USER new_user CREATEDB;

    GRANT ALL PRIVILEGES ON DATABASE your_database TO new_user;

Exit `psql` from customer utility

    /q

In the container `backend`, execute the command to perform migrations

    3. docker compose exec backend python manage.py migrate

In the container `backend`, execute a command to collect all static files

    4. docker compose exec backend python manage.py collectstatic

Recreate docker-compose:

    5. docker compose up -- build

`To use the admin panel, follow the next command in the container "backend":`
(Follow the finished steps)
 
    python manage.py createsuperuser

### It is possible to use the `API interface`
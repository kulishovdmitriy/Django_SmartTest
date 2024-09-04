# Application Smart Test

### Annex for various tests

## Install app

It is assumed that you have docker/docker-compose.
The following steps for deploying the application:

    1. git pull

If you want to launch a local application without DoCker/Docker-Compose, you need to create a virtual environment (commands for Linux)

If you want to start from docker-compose, miss these steps

    python3 -m venv venv
    source ./venv/bin/activate

Set addictions from requirements.txt

    pip install -r requirements.txt

Create a file `.env` as described in the example `.env.example` and fill in your values

In file `.env` you can switch between `dev` and `prod`:

    RUN_MODE=

Follow the starting command for `docker-compose`

    2. docker compose up -- build

In the container `backend`, execute the command to perform migrations

    3. docker compose exec backend python manage.py migrate

In the container `backend`, execute a command to collect all static files

    4. docker compose exec backend python manage.py collectstatic

In the container `postgres`,follow the command to create a new user.
Here `psql` - is a customer utility for PostgreSQL, and `-U postgres` indicates that you are in as a super - user Postgressql `postgres`.
Replace `your_database` and `new_user`. 

    5. docker compose exec postgres psql -U postgres
    
    6. CREATE USER new_user WITH PASSWORD 'password123'

    7. ALTER USER new_user CREATEDB;

    8. GRANT ALL PRIVILEGES ON DATABASE your_database TO new_user;

Exit `psql` from customer utility

    /q

Recreate docker-compose:

    docker compose up -- build



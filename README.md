# Application Smart Test

### Annex for various tests

## Install app

It is assumed that you have docker/docker-compose.
The following steps for deploying the application:

    1. git pull

If you want to launch a local application without Docker/Docker-Compose, you need to create a virtual environment (commands for Linux)

If you want to start from docker-compose, miss these steps

    python3 -m venv venv
    source ./venv/bin/activate

Set addictions from requirements.txt

    pip install -r requirements.txt

Create a file `.env` as described in the example `.env.example` and fill in your values

In file `.env` you can switch between `dev`, `staging` or `prod`:

    RUN_MODE=

Before launching containers, make these lines in file `nginx/default.conf` :

    2. #limit_req zone=mylimit burst=5 nodelay;
       #limit_req_status 429;

Follow the starting command for `docker-compose`

    3. docker compose up -- build

In the container `nginx`, execute the command to install limits in requests:

    4. docker compose exec nginx sh
    5. vi /etc/nginx/nginx.conf

Add this code `limit_req_zone $binary_remote_addr zone=mylimit:10m rate=1r/s;` as an example and save changes

    http {

    limit_req_zone $binary_remote_addr zone=mylimit:10m rate=1r/s;
    

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    ...

leave the container, report the lines:

    6. limit_req zone=mylimit burst=5 nodelay;
    7. limit_req_status 429;

Reload container.

In the container `backend`, execute the command to perform migrations

    8. docker compose exec backend python manage.py migrate

In the container `backend`, execute a command to collect all static files

    9. docker compose exec backend python manage.py collectstatic

In the container `postgres`,follow the command to create a new user.
Here `psql` - is a customer utility for PostgreSQL, and `-U postgres` indicates that you are in as a super - user Postgressql `postgres`.
Replace `your_database` and `new_user`. 

    10. docker compose exec postgres psql -U postgres
    
    11. CREATE USER new_user WITH PASSWORD 'password123'

    12. ALTER USER new_user CREATEDB;

    13. GRANT ALL PRIVILEGES ON DATABASE your_database TO new_user;

Exit `psql` from customer utility

    /q

Recreate docker-compose:

    14. docker compose up -- build



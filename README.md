# Booking API

### Description

This is a simple api for booking hotels. You can create, read, update and delete rooms, facilities for this rooms, hotels with rooms and book concrete rooms if available.

# How to run

You can run this project either using Docker or not.

### Using docker-compose

The best way is to run this project using `docker-compose`. You just need `Docker` to be installed installed on your machine. The best way is to install `Docker Desktop` using [official guide](https://docs.docker.com/desktop/).

Once you have installed and run `Docker Desktop` you need to run `Redis` and `PostgreSQL` containers:

```bash
docker run --name booking_cache \
    -p 7379:6379 \
    --network=booking_network \
    -d redis

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=<posgres_user_name> \
    -e POSTGRES_PASSWORD=<postgres_user_pass> \
    -e POSTGRES_DB=booking \
    --network=booking_network \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres
```

If you want to use `Nginx` as a proxy to your server, run the followind command:

```bash
docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --network=booking_network \
    --rm -d -p 80:80 nginx
```

If not, you need to specify the ports in the `docker-compose.yml`:

```yml
services:
  booking_backend_service:
    container_name: 'booking_backend'
    ports:
      7777:8000
    ... 
```

Now create needed .env files. Make sure `<posgres_user_name>` and `<postgres_user_pass>` have the same values as in `docker run` command.

```
# .env
MODE = LOCAL

DB_NAME = booking
DB_HOST = booking_db
DB_USER = <postgres_user_name>
DB_PASS = <postgres_user_pass>
DB_PORT = 5432

REDIS_HOST = booking_cache
REDIS_PORT = 6379

-----------
# .env.test
MODE = TEST

DB_NAME = test_booking
DB_HOST = booking_db
DB_USER = <postgres_user_name>
DB_PASS = <postgres_user_pass>
DB_PORT = 5432

REDIS_HOST = booking_cache
REDIS_PORT = 6379

-----------
# /path/to/the/project/src/auth/.env
JWT_SECRET = <jwt-secret> # opensll rand -hex 32
JWT_ALG = HS256
ACCESS_TOKEN_EXP_MINUTES = 30
REFRESH_TOKEN_EXP_MINUTES = 30
```

Once you've done with all above, just run:

```bash
docker-compose up -d
```

If you used `Nginx`, then go to `localhost`, if not, go to `localhost:7777`.

If you change `nginx.conf` file, restart container:

```
docker exec booking_nginx nginx -s reload
```


### Using Docker

This repository contains Dockerfile, you can run this project using it.

Make sure you installed `Docker` on your machine. The best way is to install `Docker Desktop` using [official guide](https://docs.docker.com/desktop/).

Once you've installed and run `Docker Desktop` you can build and run this project using `Dockerfile`:

```bash
docker build -t booking-image .
```

This command will generate image based on `Dockerfile`. 

Then you need to create a docker network using:

```bash
docker network create booking_network
```

Next you need to run Redis and PostgreSQL using `Docker`:

```bash
docker run --name booking_cache \
    -p 7379:6379 \
    --network=booking_network \
    -d redis

docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=<posgres_user_name> \
    -e POSTGRES_PASSWORD=<postgres_user_pass> \
    -e POSTGRES_DB=booking \
    --network=booking_network \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres
```

This commands will run docker containers with `Redis` and `PostgreSQL` using latest versions. 

Next create .env file in the root directory of the project. Fill it with according to .env.example file. Make sure `<posgres_user_name>` and `<postgres_user_pass>` have the same values.

```
MODE = LOCAL

DB_NAME = booking
DB_HOST = booking_db
DB_USER = <posgres_user_name>
DB_PASS = <postgres_user_pass>
DB_PORT = 6432
REDIS_HOST = booking_cache
REDIS_PORT = 7379
```

Then you can run the container based on this image using:

```bash
docker run --name booking_backend \
    -p 7777:8000 \
    --network=booking_network \
    booking-image
```

The API will be available on `0.0.0.0:7777`.

For the `celery` support run the following:

```bash
docker run --name booking_celery_worker \
    --network=booking_network \
    booking-image \
    celery --app=src.core.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_celery_beat \
    --network=booking_network \
    booking-image \
    celery --app=src.core.tasks.celery_app:celery_instance worker -l INFO -B
```


### Without Docker

Make sure PostgreSQL and Redis is running:

MacOS:
```bash
brew install postgresql
brew services start postgresql
# for stopping use:
# brew services stop postgresql 

brew install redis
brew services start redis
# for stopping use:
# brew services stop redis
```

For more information go to [Postgresql](https://www.postgresql.org/download/macosx/) and [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/install-redis-on-mac-os/). 

Next you need create a 'booking' table and 'test_booking' table for running tests. You can do it using, for example, [DBeaver](https://dbeaver.io/), or via command-line:

```bash
psql -h localhost -p 5432 -U postgres
create database booking;
create database test_booking;
\q
```

You can change the names of databases, but don't forget to change .env file (will be explained further).

Next create .env file in the root directory of the project. Fill it with according to .env.example file. For default parameters you can use this file:

```
MODE = LOCAL

DB_NAME = booking
DB_HOST = localhost
DB_USER = postgres
DB_PASS = postgres
DB_PORT = 5432
REDIS_HOST = localhost
REDIS_PORT = 6379
```

Make sure to change necessary parameters according to previous steps. 

Then create .env.test file according to the .test.env.example file in the root directory of the project. This will be used for testing using `pytest`.


Next create .env file in the directory ```/path/to/project/src/auth/``` anf fill it according to .env.example file in the corresponding directory. 

```
JWT_SECRET = <your-jwt-secret> 
JWT_ALG = HS256
JWT_EXP = 30

REFRESH_TOKEN_KEY = <your-refresh-token-key>
REFRESH_TOKEN_EXP = 30days
```

For ```JWT_SECRET``` and ```REFRESH_TOKEN_KEY``` you can use next command in your shell:
```
openssl rand -hex 32
```

This will output rundom secret_key for jwt encoding.

Next make sure you created virtual env and installed necessary dependencies. Run following commands in the root directory of the project:

```bash
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -r requirements.txt
```

Next make migrations using `Alembic`:

```bash
alembic upgrade head
```

Now you're ready to start. Run the following commang in the root directory of the project:

```bash
python3 src/main.py
```


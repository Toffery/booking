## 0. About

**Booking** is a simple async API using FastAPI, Pydantic V2, SQLAlchemy 2.0 and PostgreSQL:

- [`FastAPI`](https://fastapi.tiangolo.com)
- [`Pydantic V2`](https://docs.pydantic.dev/2.4/)
- [`SQLAlchemy 2.0`](https://docs.sqlalchemy.org/en/20/changelog/whatsnew_20.html)
- [`PostgreSQL`](https://www.postgresql.org)
- [`Redis`](https://redis.io)
- [`Docker Compose`](https://docs.docker.com/compose/)
- [`NGINX`](https://nginx.org/en/)

## 1. Contents

0. [About](#0-about)
1. [Contents](#1-contents)
2. [Prerequisites](#2-prerequisites)

## 2. Prerequisites

Clone this repository 
```sh
git clone https://github.com/Toffery/booking.git
```

Create `.env`, `.test.env` in the root directory of the project and `/path/to/project/auth/.env` files. The project structure will look like this (assuming booking is the root directory of the project):

```sh
booking
├── migrations/
│   ├── ...
├── src/
│   ├── auth/
│      ├──  __init__.py
│      ├── .env
│      ├── .env.example
│      ├── ...
│   ├── bookings/
│   ├── ...
├── tests/
│   ├── ...
├── ...
├── .env
├── .env.example
├── ...
├── .test.env
├── .test.env.example
└── ...
```

Fill them according to the example files or look at the example below:

```
# .env
MODE = LOCAL

DB_NAME = booking
DB_HOST = localhost # paste container_name if using docker (default booking_postgres)
DB_USER = <postgres_user_name>
DB_PASS = <postgres_user_pass>
DB_PORT = 5432

REDIS_HOST = localhost # paste container_name if using docker (default booking_redis)
REDIS_PORT = 6379

-----------
# .env.test
MODE = TEST

DB_NAME = test_booking
DB_HOST = localhost # paste container_name if using docker (default booking_postgres)
DB_USER = <postgres_user_name>
DB_PASS = <postgres_user_pass>
DB_PORT = 5432

REDIS_HOST = localhost # paste container_name if using docker (default booking_redis)
REDIS_PORT = 6379

-----------
# /path/to/the/project/src/auth/.env
JWT_SECRET = <jwt-secret> # opensll rand -hex 32
JWT_ALG = HS256
ACCESS_TOKEN_EXP_MINUTES = 30
REFRESH_TOKEN_EXP_MINUTES = 30
```
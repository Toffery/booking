docker run --name booking_db \
    -p 6432:5432 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=booking \
    --network=my-network \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres

docker run --name booking_cache \
    -p 7379:6379 \
    --network=my-network \
    -d redis

docker run --name booking_backend \
    -p 7777:8000 \
    --network=my-network \
    booking-image

docker run --name booking_celery_worker \
    --network=my-network \
    booking-image \
    celery --app=src.core.tasks.celery_app:celery_instance worker -l INFO

docker run --name booking_celery_beat \
    --network=my-network \
    booking-image \
    celery --app=src.core.tasks.celery_app:celery_instance worker -l INFO -B

docker run --name booking_nginx \
    --volume ./nginx.conf:/etc/nginx/nginx.conf \
    --volume /etc/letsencrypt:/etc/letsencrypt \
    --volume /var/lib/letsencrypt:/var/lib/letsencrypt \
    --network=my-network \
    --rm -d -p 80:80 -p 443:443 nginx

docker build -t booking-image .


Certificate is saved at: /etc/letsencrypt/live/mrtoffery.ru/fullchain.pem
Key is saved at:         /etc/letsencrypt/live/mrtoffery.ru/privkey.pem

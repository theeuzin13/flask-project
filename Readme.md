## Command to access database

>- docker exec -it flask_mysql mysql -uroot -proot

## To access application to run migration

>- docker exec -it flask_app bash
>- flask db init
>- flask db migrate -m "initial tables"
>- flask db upgrade

## To up with cloudflared tunnel

>- docker compose up --build -d
>- cloudflared tunnel run flask-project || cloudflared tunnel --config ~/.cloudflared/config.yml run flask-project

## Endpoint

>- https://dev.agendfy.shop/login

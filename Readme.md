## Command to access database

>- docker exec -it flask_mysql mysql -uroot -proot

## To access application to run migration

>- docker exec -it flask_app bash
>- flask db init
>- flask db migrate -m "initial tables"
>- flask db upgrade

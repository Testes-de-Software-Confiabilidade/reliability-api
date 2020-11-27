postgres_id=$(docker ps -aqf "name=reliability_db_1")
docker exec -it $postgres_id bash
psql -U postgres
create database reliability;
\q
exit
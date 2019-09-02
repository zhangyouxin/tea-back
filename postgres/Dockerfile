FROM postgres:alpine

WORKDIR postgres

COPY sql/init.sql /docker-entrypoint-initdb.d/init.sql

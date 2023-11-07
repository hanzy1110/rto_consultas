#!/bin/bash
set -x
git pull

function build_dev() {
    sudo docker-compose -f docker-compose.dev.yml --env-file envfiles/.env rm -sv --force rto_consultas_dev
    sudo docker-compose -f docker-compose.dev.yml --env-file envfiles/.env build
    sudo docker-compose -f docker-compose.dev.yml --env-file envfiles/.env up -d
    return 0
}

function build_nginx() {
    sudo docker-compose --env-file envfiles/.env.prod rm -sv --force rto_consultas_web_server
    sudo docker-compose --env-file envfiles/.env.prod build
    sudo docker-compose --env-file envfiles/.env.prod up -d
    return 0
}

function build_prod() {
    # sudo docker-compose --env-file envfiles/.env.prod down --remove-orphans
    sudo docker-compose --env-file envfiles/.env.prod rm -sv --force rto_consultas_prod
    sudo docker-compose --env-file envfiles/.env.prod rm -sv --force rto_consultas_web_server
    sudo docker-compose --env-file envfiles/.env.prod build
    sudo docker-compose --env-file envfiles/.env.prod up -d
    return 0
}

if [ "$1" == "dev" ]; then
    build_dev ""
elif [ "$1" == "prod" ]; then
    build_prod ""

elif [ "$1" == "all" ]; then
    build_dev ""
    build_prod ""
elif [ "$1" == "nginx" ]; then
    build_nginx ""
fi

sudo docker ps -a

#!/bin/zsh

source ~/.zshrc
awslocal sqs create-queue --queue-name em-preparacao-pizzaria --region us-east-1
awslocal sqs create-queue --queue-name pronto-pizzaria --region us-east-1

awslocal dynamodb create-table \
    --table-name pedidos-pizzaria \
    --attribute-definitions AttributeName=pedido,AttributeType=S AttributeName=datetime,AttributeType=S\
    --key-schema AttributeName=pedido,KeyType=HASH AttributeName=datetime,KeyType=RANGE \
    --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 \
    --region us-east-1

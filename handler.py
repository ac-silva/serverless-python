import os
import json
import boto3
import datetime
from sqsHandler import SqsHandler

def s3Handler(event, context):
    record = event['Records'][0]
    file = record['s3']['object']['key']

    sqsPreparacao = SqsHandler(os.environ.get('SQS_PREPARACAO_URL', ''))
    sqsPronto = SqsHandler(os.environ.get('SQS_PRONTO_URL', ''))

    # file = ${status}/${pedido}-{cliente}"
    filename_splited = file.split("/")
    status = filename_splited[0]
    pedido_and_cliente = filename_splited[1].split("-")
    pedido = pedido_and_cliente[0]
    cliente = pedido_and_cliente[1]

    message = json.dumps({
        "pedido": pedido,
        "datetime": str(datetime.datetime.now().replace(microsecond=0).isoformat()) + "Z",
        "cliente": cliente,
        "status": status
    })

    if (status == "em-preparacao"):
        sqsPreparacao.send(message)
    else:
        sqsPronto.send(message)


def sqsHandler(event, context):
    record = event['Records'][0]
    message = json.loads(record['body'])
    table = boto3.resource('dynamodb').Table(os.environ.get('DYNAMODB_TABLE', ''))
    table.put_item(Item=message)


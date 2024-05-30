import os
import json
import boto3
import datetime
from sqsHandler import SqsHandler

def s3Handler(event, context):
    record = event['Records'][0]
    filename = record['s3']['object']['key']

    sqsPreparacao = SqsHandler(os.environ.get('SQS_PREPARACAO_URL', ''))
    sqsPronto = SqsHandler(os.environ.get('SQS_PRONTO_URL', ''))

    # file = ${status}/${pedido}-{cliente}"
    filename_splited = filename.split("/")
    status = filename_splited[0]

    message = json.dumps({
        "filename": filename_splited[1]
    })

    if (status == "em-preparacao"):
        sqsPreparacao.send(message)
    else:
        sqsPronto.send(message)

def store_in_dynamodb(filename, status):
    pedido_and_cliente = filename.split("-")
    pedido = pedido_and_cliente[0]
    cliente = pedido_and_cliente[1]

    message = {
        "pedido": pedido,
        "datetime": str(datetime.datetime.now().replace(microsecond=0).isoformat()) + "Z",
        "cliente": cliente,
        "status": status
    }

    table = boto3.resource('dynamodb').Table(os.environ.get('DYNAMODB_TABLE', ''))
    table.put_item(Item=message)

def sqsPreparacaoHandler(event, context):
    record = event['Records'][0]
    message = json.loads(record['body'])
    filename = message['filename']
    store_in_dynamodb(filename, "em-preparacao")
    
def sqsProntoHandler(event, context):
    record = event['Records'][0]
    message = json.loads(record['body'])
    filename = str(message['filename'])
    store_in_dynamodb(filename, "pronto")

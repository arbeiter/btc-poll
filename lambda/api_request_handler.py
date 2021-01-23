import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
import statistics
from producer.metric_gatherer import MetricsGatherer

def get_table():
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    # set environment variable
    TABLE_NAME = os.environ['TABLE_NAME']
    table = dynamodb.Table(TABLE_NAME)
    return table

def route_request(resource, path, path_params):
    table = get_table()
    metric_gatherer = MetricsGatherer()
    if resource == '/':
        return metric_gatherer.get_all_keys()
    elif resource == '/metrics':
        return ""
    elif resource == "/metrics/{id}":
        key = path_params["id"]
        return metric_gatherer.get_metrics(key)
    elif resource == "/rank/{id}":
        key = path_params["id"]
        return metric_gatherer.get_rank(key)
    else:
        return "Resource Not Found"

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    resource = event['resource']
    path = event['path']
    path_params = event['pathParameters']
    response = route_request(resource, path, path_params)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': response
    }

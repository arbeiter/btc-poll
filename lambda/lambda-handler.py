import json
import boto3


def route_request(resource, path, path_params):
    pass

def get_metrics(key):
    # make ddb call
    # fetch list
    # get 24 hour records: 24 * 60 * 60 -> records
    # if < 24 * 60 * 60, get all records
    pass

def get_rank(key):
    pass

def get_all_keys():
    pass

def handler(event, context):
    print('request: {}'.format(json.dumps(event)))

    resource = event['resource']
    path = event['path']
    path_params = event['pathParameters']
    route_request(resource, path, path_params)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/plain'
        },
        'body': 'Hello, CDK! You have hit {}\n'.format(event['path'])
    }

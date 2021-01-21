from __future__ import print_function
import json
import requests
import uuid
import decimal
import os
import boto3


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# set environment variable
TABLE_NAME = os.environ['TABLE_NAME']
coins = ["btcusd", "ltcusd", "dogeusd"]

def fetch_coin_price(coin_name):
    url = f"https://api.cryptowat.ch/markets/kraken/{coin_name}/price"
    r = requests.get('url')
    return r.json()['result']['price']

def write_to_ddb(coin_name, coin_price):
    pass

def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    for coin in coins:
        fetch_coin_price(coin)

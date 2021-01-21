from __future__ import print_function
import json
import urllib3
import uuid
import decimal
import os
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# set environment variable
TABLE_NAME = os.environ['TABLE_NAME']
coins = ["btcusd", "ltcusd", "dogeusd"]

def fetch_coin_price(coin_name):
    url = f"https://api.cryptowat.ch/markets/kraken/{coin_name}/price"
    http = urllib3.PoolManager()
    r = http.request('GET', url)
    price = json.loads(r.data)['result']['price']
    return price

def write_to_ddb(coin_name, coin_price):
    table = dynamodb.Table(TABLE_NAME)
    response = table.update_item(
        Key={id: coin_name},
        UpdateExpression='set #prices = list_append(if_not_exists(#prices, :empty_list), :price)',
        ExpressionAttributeNames={
          '#prices': 'prices'
        },
        ExpressionAttributeValues={
          ':price': [str(coin_price)],
          ':empty_list': []
        },
        ReturnValues='ALL_NEW')
    print(response)

def lambda_handler(event, context):
    for coin in coins:
        price = fetch_coin_price(coin)
        write_to_ddb(coin, price)

from __future__ import print_function
import json
import urllib3
import uuid
import decimal
import os
import boto3
from lambda_handler import MetricsGatherer
import statistics

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

def generate_alerts(coin_name, coin_price):
    metrics_gatherer = MetricsGatherer()
    day_metrics = metrics_gatherer.get_day_metrics(coin_name)
    hour_metrics = day_metrics[(-1 * 60 * 60):]
    mean = statistics.mean(hour_metrics)
    if coin_price > 3 * mean:
        print("Alert " + coin_price + " " + coin_name)

def write_to_ddb(coin_name, coin_price):
    table = dynamodb.Table(TABLE_NAME)
    response = table.update_item(
        Key={'id': coin_name},
        UpdateExpression='set #prices = list_append(if_not_exists(#prices, :empty_list), :price)',
        ExpressionAttributeNames={
          '#prices': 'prices'
        },
        ExpressionAttributeValues={
          ':price': [str(coin_price)],
          ':empty_list': []
        },
        ReturnValues='ALL_NEW')
    generate_alerts(coin_name, coin_price)

def lambda_handler(event, context):
    for coin in coins:
        price = fetch_coin_price(coin)
        write_to_ddb(coin, price)

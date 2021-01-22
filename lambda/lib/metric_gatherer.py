import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
import statistics

def get_table():
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    # set environment variable
    TABLE_NAME = os.environ['TABLE_NAME']
    table = dynamodb.Table(TABLE_NAME)
    return table

class MetricsGatherer:
    def __init__(self):
        self.table = get_table()

    def get_day_metrics(self, ids):
        seconds_in_day = 24 * 60 * 60
        if len(ids) < seconds_in_day:
            return str(ids)
        print(ids)
        return str(ids[(-1 * seconds_in_day):])

    def get_metrics(self, key):
        all_metrics = self.table.query(KeyConditionExpression=Key('id').eq(key))
        ids = all_metrics['Items']
        all_ids = ids[0]['prices']
        return self.get_day_metrics(all_ids)

    def get_all_metrics(self):
        result = self.table.scan()
        data = result['Items']
        result = {}
        for item in data:
            coin_id = item['id']
            prices = item['prices']
            result[coin_id] = prices
        return result

    def get_all_keys(self):
        keys = self.get_all_metrics().keys()
        return str(keys)

    def get_rank(self, requested_key):
        all_metrics = self.get_all_metrics()
        keys = all_metrics.keys()
        std_dev_map = {}
        last_second_val_map = {}

        for key in keys:
            prices = all_metrics[key]
            prices = [float(i) for i in prices]

            std_dev = statistics.stdev(prices)
            std_dev_map[key] = std_dev
            last_second_val_map[key] = prices[-1]
        ranked_keys = sorted(std_dev_map, key=std_dev_map.get)
        return str(ranked_keys.index(requested_key))

"""
module ge.predix
By Adi Suresh
"""
import json
import pika
import requests
import yaml
import redis
import boto3
import os
from ge.data.sql import PostgreSQL
from ge.data.utilities import get_proxy


class AssetData:
    headers = None
    base_url = None

    def __init__(self, instance_id, token, base_url='https://predix-asset.run.aws-usw02-pr.ice.predix.io/'):
        self.headers = {'Content-Type': 'application/json;charSet=utf-8',
                        'Authorization': 'bearer ' + token,
                        'Predix-Zone-Id': instance_id}
        self.base_url = base_url

    def audit(self, filters=None, page_size=None):
        page_size_string = ""
        filter_string = ""
        if filters is not None and type(filters).__name__ == "dict":
            filter_strings = []
            for key in filters.keys():
                filter_strings.append("=".join([key, filters[key]]))
            filter_string = "filter=" + ":".join(filter_strings)
        if page_size is not None:
            page_size_string = "pageSize="+str(page_size)
        url = self.base_url + "system/audit?" + _combine([filter_string, page_size_string])
        r = requests.get(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def delete(self, item):
        url = self.base_url + item
        r = requests.delete(url, proxies=get_proxy(), headers=self.headers)
        r.raise_for_status()

    def get(self, item, filters=None, fields=None, page_size=None):
        filter_string = ""
        field_string = ""
        page_size_string = ""
        if filters is not None and type(filters).__name__ =="dict":
            filter_strings = []
            for key in filters.keys():
                filter_strings.append("=".join([key, filters[key]]))
            filter_string = "filter=" + ":".join(filter_strings)
        if fields is not None and type(fields).__name__ in ["list", "tuple"]:
            field_string = "fields=" + ",".join(fields)
        if page_size is not None:
            page_size_string = "pageSize=" + str(page_size)
        url = self.base_url + item + "?" + _combine([filter_string, field_string, page_size_string])
        r = requests.get(url, proxies=get_proxy(), headers=self.headers,)
        r.raise_for_status()
        return yaml.safe_load(json.dumps(r.json()))

    def post(self, item, data):
        json_data = json.JSONEncoder().encode(data)
        r = requests.post(self.base_url + item,
                          proxies=get_proxy(), headers=self.headers, data=json_data)
        r.raise_for_status()

    def __str__(self):
        return "AssetData instance "+self.headers['Predix-Zone-Id']


class TimeSeries:
    def __init__(self,
                 instance_id,
                 token,
                 ingest_url='wss://gateway-predix-data-services.run.aws-usw02-pr.ice.predix.io/v1/stream/messages',
                 query_url='https://time-series-store-predix.run.aws-usw02-pr.ice.predix.io/v1/datapoints'):
        self.headers = {'Content-Type': 'application/json',
                        'Authorization': 'bearer ' + token,
                        'Predix-Zone-Id': instance_id}
        self.ingest_url = ingest_url
        self.query_url = query_url

    def ingest(self, data):
        json_data = json.JSONEncoder().encode(data)
        r = requests.get(self.ingest_url, proxies=get_proxy(), headers=self.headers, data=json_data)
        r.raise_for_status()

    def query(self, query):
        json_data = json.JSONEncoder().encode(query)
        r = requests.post(self.ingest_url, proxies=get_proxy(), headers=self.headers, data=json_data)
        r.raise_for_status()

    def __str__(self):
        return "TimeSeries instance " + self.headers['Predix-Zone-Id']


class MessageQueue:
    def __init__(self, host):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

    def close(self):
        self.connection.close()

    def create_exchange(self, exchange, **kwargs):
        self.channel.exchange_declare(exchange=exchange, **kwargs)

    def create_queue(self, queue, bindings=None):
        self.channel.queue_declare(queue=queue, durable=True)
        if bindings is not None:
            self.channel.queue_bind(**bindings)

    def receive(self, callback, queue):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(callback,
                              queue=queue)
        self.channel.start_consuming()

    def send(self, queue, message, exchange='', properties={}):
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(exchange=exchange,
                              routing_key=queue,
                              body=message,
                              properties = pika.BasicProperties(**properties))


class KeyValueStore(redis.StrictRedis):
    def __init__(self, **kwargs):
        redis.StrictRedis.__init__(self, **kwargs)


class SQLDatabase(PostgreSQL):
    def __init__(self, host, database, user, password):
        PostgreSQL.__init__(self, host=host, database=database, user=user, password=password)


class Blobstore:
    def __init__(self, access_key_id, secret_access_key, bucket_name):
        os.environ['AWS_ACCESS_KEY_ID'] = access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] =secret_access_key
        self.bucket = boto3.resource('s3').Bucket(bucket_name)

    def get(self, filename, target_filename):
        self.bucket.download_file(filename, target_filename)

    def put(self, filename, data):
        self.bucket.put_object(key=filename, body=data)


def _combine(a):
    terms_of_length = filter(lambda x: len(x) > 0, a)
    if len(terms_of_length) == 0:
        return ""
    elif len(terms_of_length) == 1:
        return terms_of_length[0]
    else:
        return "&".join(terms_of_length)




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
from predix import get_proxy


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
        self.db = psycopg2.connect(host=host, database=database, user=user, password=password)

    # create table
    # connect_string:  <user>/<password>@<hostname>/<service name>
    # table: table name
    # new_output_data: list of rows of test_data
    # new_output_headers: list of headers corresponding to list of rows
    # unique_name: constraint name
    # unique_terms: unique column constraint
    def create(self, table, new_output_data, new_output_headers, unique_name=None, unique_terms=None):
        data, headers = transform_data_structure(new_output_data, new_output_headers)
        cursor = self.db.cursor()
        create_terms = []

        for index, element in enumerate(data[0]):
            create_terms.append(headers[index].upper() + " " + _get_postgres_type(element))

        create_statement = "CREATE TABLE " + table + "( " + ", ".join(create_terms)
        if unique_name is not None and unique_terms is not None:
            create_statement += ", CONSTRAINT " + unique_name + " UNIQUE " + str(tuple(unique_terms)) + ");"
        else:
            create_statement += ")"

        print create_statement
        cursor.execute(create_statement)
        self.insert(table, data, headers)
        self.db.commit()
        cursor.close()
        self.db.close()

    # drop table from Oracle database
    # connect_string:  <user>/<password>@<hostname>/<service name>
    # table: table name
    # cascade_constraints: delete attached constraints?
    # purge: purge test_data in database?
    def drop(self, table, cascade_constraints=True, purge=True):
        cursor = self.db.cursor()
        drop_statement = "DROP TABLE " + table
        if cascade_constraints:
            drop_statement += " CASCADE CONSTRAINTS"

        if purge:
            drop_statement += " PURGE"

        drop_statement += ";"
        cursor.execute(drop_statement)
        self.db.commit()
        cursor.close()
        self.db.close()

    def execute(self, statement):
        cursor = self.db.cursor()
        output = None
        cursor.execute(statement)
        if 'SELECT' in statement:
            output = cursor.fetchall()
        self.db.commit()
        cursor.close()
        self.db.close()
        if output is not None:
            return output

    # insert row into table
    # connect_string:  <user>/<password>@<hostname>/<service name>
    # table: table name
    # new_output_data: list of rows of test_data
    # new_output_headers: list of headers corresponding to list of rows
    def insert(self, table, new_output_data, new_output_headers):
        data, headers = transform_data_structure(new_output_data, new_output_headers)
        cursor = self.db.cursor()
        new_headers = []
        new_header_string = ", ".join(headers)
        for row in data:
            new_values = []
            for index, header in enumerate(headers):
                if _get_postgres_type(row[index]) == "DATE":
                    new_values.append("TO_TIMESTAMP('" + row[index].strftime("%m/%d/%Y")+"', 'MM/DD/YYYY')")
                elif _get_postgres_type(row[index]) == "TIMESTAMP":
                    new_values.append("TO_TIMESTAMP('" + row[index].strftime("%m/%d/%Y %H:%M:%S") + "', 'MM/DD/YYYY HH24:MI:SS')")
                elif _get_postgres_type(row[index]) == 'JSONB':
                    new_values.append("'" + json.dumps(row[index]) + "'")
                else:
                    new_values.append("'" + str(row[index]) + "'")

            insert_statement = "INSERT INTO " + table + " (" + new_header_string + ") VALUES (" + ", ".join(
                new_values) + ")"
            cursor.execute(insert_statement)

        self.db.commit()
        cursor.close()
        self.db.close()

    # select row from table
    # connect_string:  <user>/<password>@<hostname>/<service name>
    # select_variables: variables to select
    # table: table name
    # filters: filters containing the WHERE clause
    def select(self, select_variables, table, filters):
        if type(select_variables).__name__ == 'str':
            select_variables = [select_variables]

        cursor = self.db.cursor()
        select_keys = []
        select_values = []
        running_index = 1
        for key in filters:
            value = filters[key]
            if type(value).__name__ in ["tuple", "list"]:
                select_key = key + " IN ("
                value = clean_escape_characters(value)
                select_key += ", ".join(value) + ")"
                select_keys.append(select_key)
            else:
                if _get_postgres_type(value) == "DATE":
                    select_keys.append(key + " = TO_TIMESTAMP('" + value.strftime("%m/%d/%Y") + "', 'MM/DD/YYYY')")
                elif _get_postgres_type(value) == "TIMESTAMP":
                    select_keys.append(key + " = TO_TIMESTAMP(:'" + value.strftime(
                        "%m/%d/%Y %H:%M:%S") + "', 'MM/DD/YYYY HH24:MI:SS')")
                elif _get_postgres_type(value) == 'JSONB':
                    select_keys.append(key + " = '" + json.dumps(value) + "'")
                else:
                    select_keys.append(key + " = '" + str(value) + "'")

                select_values.append(str(value))
                running_index += 1

        select_statement = "SELECT DISTINCT " + ", ".join(
            select_variables) + " FROM " + table + " WHERE " + " AND ".join(select_keys)
        cursor.execute(select_statement)
        output = cursor.fetchall()
        self.db.commit()
        cursor.close()
        self.db.close()
        return output

    # update row in table
    # connect_string:  <user>/<password>@<hostname>/<service name>
    # table: table name
    # pk_id: id of primary key
    # pk_value: value of primary key
    # new_output_data: list of rows of test_data
    # new_output_headers: list of headers corresponding to list of rows
    def update(self, table, new_output_data, new_output_headers, select_data, select_headers):
        data, headers = transform_data_structure(new_output_data, new_output_headers)
        where_data, where_headers = transform_data_structure(select_data, select_headers)
        cursor = self.db.cursor()
        for row in data:
            update_strings = []
            for index, header in enumerate(headers):
                if _get_postgres_type(row[index]) == "DATE":
                    update_strings.append(
                        str(header) + " = TO_DATE('" + row[index].strftime('%m/%d/%Y') + "', 'MM/DD/YYYY')")
                elif _get_postgres_type(row[index]) == "TIMESTAMP":
                    update_strings.append(str(header) + " = TO_TIMESTAMP('" + row[index].strftime(
                        "%m/%d/%Y %H:%M:%S") + "', 'MM/DD/YYYY HH24:MI:SS')")
                elif _get_postgres_type(row[index]) == 'JSONB':
                    update_strings.append(str(header) + " = '" + json.dumps(row[index]) + "'")
                else:
                    update_strings.append(str(header) + " = '" + str(row[index]) + "'")
            where_strings = []
            for index, header in enumerate(where_headers):
                if _get_postgres_type(where_data[0][index]) == "DATE":
                    where_strings.append(str(header) + " = TO_DATE(" + where_data[0][index] + ", 'MM/DD/YYYY')")
                elif _get_postgres_type(where_data[0][index]) == "TIMESTAMP":
                    where_strings.append(
                        str(header) + " = TO_TIMESTAMP(" + where_data[0][index] + ", 'MM/DD/YYYY HH24:MI:SS')")
                elif _get_postgres_type(where_data[0][index]) == "NUMBER":
                    where_strings.append(str(header) + " = " + where_data[0][index])
                elif _get_postgres_type(where_data[0][index]) == 'JSONB':
                    where_strings.append(str(header) + " = '" + json.dumps(where_data[0][index]) + "'")
                else:
                    where_strings.append(str(header) + " = '" + where_data[0][index] + "'")

            update_statement = "UPDATE " + table + " SET " + ", ".join(update_strings) + " WHERE " + " AND ".join(
                where_strings)
            cursor.execute(update_statement, tuple(row))

        self.db.commit()
        cursor.close()
        self.db.close()


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


def _get_postgres_type(variable):
    if type(variable).__name__ in ['int', 'float', 'long', 'complex']:
        return "NUMERIC"
    elif type(variable).__name__ in ["datetime", "date"]:
        return "TIMESTAMP"
    elif type(variable).__name__ == "str":
        return "VARCHAR(255)"
    elif type(variable).__name__ == "bool":
        return "BOOLEAN"
    elif type(variable).__name__ == 'dict':
        return 'JSONB'
    else:
        print variable
        print type(variable).__name__
        raise Exception("Invalid test_data type. Supported test_data Types are numbers, datetime.datetime, "
                        "datetime.date, strings, boolean and dictionaries (binary json)")

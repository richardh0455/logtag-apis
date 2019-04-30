import psycopg2
import json
import os

host  = os.environ['RDS_HOST']
port = os.environ['PORT']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']


def done(response):
    return {
        'statusCode': '200',
        'body': response,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Origin': '*'
        }
    }

def fail():
    return {
        'statusCode': '406',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Origin': '*'
        }
    }

def lambda_handler(event, context):
    connection = psycopg2.connect(user=username,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=db_name)
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT \"CurrencyID\", \"ShortName\" FROM public.\"Currency\"")
        ##cursor.execute("SELECT * FROM (VALUES (0, 'USD'), (1, 'HKD'), (2, 'NZD')) t1 (c1, c2) ")
        list = []
        for row in cursor.fetchall():
            list.append(parse_row(row))
        result = '['
        result += ','.join(list)
        result += ']'
        connection.commit()
        cursor.close()
        return done(result)
    except:
        return fail()

def parse_row(row):
    result = '{'
    result += "\"ID\":\""+str(row[0])+"\","
    result += "\"ShortName\":\""+row[1]+"\""
    result += '}'
    return result

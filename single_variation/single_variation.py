import psycopg2
import json
import os

host  = os.environ['RDS_HOST']
port = os.environ['PORT']
username = os.environ['USERNAME']
password = os.environ['PASSWORD']
db_name = os.environ['DB_NAME']
connection = psycopg2.connect(user=username,
                              password=password,
                              host=host,
                              port=port,
                              database=db_name)


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

def lambda_handler(event, context):
    cursor = connection.cursor()
    cursor.execute("SELECT \"Description\", \"Price\" FROM public.\"ProductConfiguration\" WHERE \"ConfigurationID\"= %s",(int(event["params"]["variation-id"]),))
    row = cursor.fetchone()
    result = parse_row(row)
    connection.commit()
    cursor.close()
    return done(result)

def parse_row(row):
    result = '{'
    result += "\"Description\":\""+row[0]+"\","
    result += "\"Price\":\""+str(row[1])+"\""
    result += '}'
    return result

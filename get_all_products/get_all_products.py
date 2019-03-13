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

def lambda_handler(event, context):
    connection = psycopg2.connect(user=username,
                                  password=password,
                                  host=host,
                                  port=port,
                                  database=db_name)
    cursor = connection.cursor()
    cursor.execute("SELECT \"ProductID\", \"Name\" FROM public.\"Product\"")
    list = []
    for row in cursor.fetchall():
        list.append(parse_row(row))
    result = '['    
    result += ','.join(list)
    result += ']'
    connection.commit()
    cursor.close()
    connection.close()
    return done(result)
    
def parse_row(row):
    result = '{'
    result += "\"ID\":\""+str(row[0])+"\","
    result += "\"Name\":\""+row[1]+"\""
    result += '}'
    return result  
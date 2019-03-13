import postgresql
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
    cursor = connection.cursor()
    try:
        id = int(event["id"])
    except:
        return fail()
    cursor.execute("SELECT * FROM public.\"Invoice\" WHERE \"InvoiceID\"= %s",(str(id),))
	##TODO:: Implement select statement 
    cursor.execute("SELECT * FROM public.\"Invoice\" WHERE \"InvoiceID\"= %s",(str(id),))
    list = []
    for row in cursor:
        list.append(parse_row(row))
    result = ','.join(list)
    connection.commit()
    cursor.close()
    connection.close()
    return done(result)
    
def parse_row(row):
    result = '{'
    for item in row.items():
        result += str(item[0]) + ':\"' + str(item[1]) + '\",'
    result += '}'
    return result    
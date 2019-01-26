import postgresql
import json

host  = "dev-logtag-sales.cm06wuycv56n.ap-southeast-2.rds.amazonaws.com"
port = '5432'
username = "logtagAdmin"
password = "a08QJ6I6u94v"
db_name = "logtag_sales"

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
    print('Received event: '+json.dumps(event))
    db = postgresql.open('pq://' + username + ':' + password + '@' + host + ':' + port + '/' + db_name)
    cursor = db.prepare("SELECT * FROM public.\"Customer\" WHERE \"CustomerID\"="+str(event.id))
    list = []
    for row in cursor:
        list.append(parse_row(row))
    result = ','.join(list)
    return done(result)
    
def parse_row(row):
    result = '{'
    for item in row.items():
        result += str(item[0]) + ':' + str(item[1]) + ','
    result += '}'
    return result    
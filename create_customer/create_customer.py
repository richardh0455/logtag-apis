import postgresql
import json

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
    db = postgresql.open('pq://' + username + ':' + password + '@' + host + ':' + port + '/' + db_name)
    cursor = db.prepare("<INSERT STATEMENT>")
    list = []
    for row in cursor:
        list.append(parse_row(row))
    result = '['    
    result += ','.join(list)
    result += ']'
    db.close()
    return done(result)
    
def parse_row(row):
    result = '{'
    items = list(row.items())
    result += "\"ID\":\""+str(items[0][1])+"\","
    result += "\"Name\":\""+items[1][1]+"\""
    result += '}'
    return result  
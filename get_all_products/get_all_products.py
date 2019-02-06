import postgresql
import json

host  = "<ELIDED>"
port = '<ELIDED>'
username = "<ELIDED>"
password = "<ELIDED>"
db_name = "<ELIDED>"

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
    cursor = db.prepare("SELECT \"ProductID\", \"Name\" FROM public.\"Product\"")
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
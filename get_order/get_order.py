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
    print('Received event: '+json.dumps(event))
    db = postgresql.open('pq://' + username + ':' + password + '@' + host + ':' + port + '/' + db_name)
    try:
        id = int(event["id"])
    except:
        return fail()
    cursor = db.prepare("<Select Statement>")
    list = []
    for row in cursor:
        list.append(parse_row(row))
    result = ','.join(list)
    db.close()
    return done(result)
    
def parse_row(row):
    result = '{'
    for item in row.items():
        result += str(item[0]) + ':\"' + str(item[1]) + '\",'
    result += '}'
    return result    
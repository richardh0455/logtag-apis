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

def lambda_handler(event, context):
    db = postgresql.open('pq://' + username + ':' + password + '@' + host + ':' + port + '/' + db_name)
    product_id = create_product(db, event["Name"],event["Description"],int(event["CostPrice"]) )
    db.close()
    return done(json.dumps('{ \"ProductID\":\"'+str(product_id)+'\"}'))
    
def create_product(db, name, description, cost_price):
    create_product = db.prepare("INSERT into public.\"Product\" (\"Name\", \"Description\", \"CostPrice\" )  VALUES ( $1, $2, $3 ) RETURNING \"ProductID\"")
    row = create_product(name, description, cost_price)
    product_id = list(row)[0][0]
    return product_id

    
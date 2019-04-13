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
    customer_id = create_customer(cursor, event["Name"],event["EmailAddress"],event["BillingAddress"], event["Region"], event["PrimaryContact"] )
    connection.commit()
    cursor.close()
    connection.close()
    return done(json.dumps('{ \"CustomerID\":\"'+str(customer_id)+'\"}'))

def create_customer(cursor, name, email, billing_address, region, primaryContact):
    cursor.execute("INSERT into public.\"Customer\" (\"Name\", \"Contact_Email\", \"Billing_Address\", \"Region\",\"Primary_Contact_Name\",\"Primary_Contact_Phone\",\"Primary_Contact_Fax\"  )  VALUES ( %s, %s, %s, %s, %s, %s, %s ) RETURNING \"CustomerID\"", (name, email, billing_address, region, primaryContact["Name"], primaryContact["Phone"], primaryContact["Fax"]))
    row = cursor.fetchone()
    return row[0]

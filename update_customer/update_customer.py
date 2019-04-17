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
    update_customer(cursor, event["CustomerID"], event["Name"],event["EmailAddress"],event["BillingAddress"], event["Region"], event["PrimaryContact"] )
    connection.commit()
    updated_rows = cursor.rowcount
    cursor.close()
    connection.close()
    return done({"AffectedRows":updated_rows})

def update_customer(cursor,customerID, name, email, billing_address, region, primaryContact):
    cursor.execute("UPDATE public.\"Customer\" SET \"Name\"= %s, \"Contact_Email\"= %s, \"Billing_Address\"= %s, \"Region\"=%s, \"Primary_Contact_Name\"=%s, \"Primary_Contact_Phone\"=%s, \"Primary_Contact_Fax\"=%s  WHERE \"CustomerID\"= %s ", (name, email, billing_address, region, primaryContact.get("Name", ""), primaryContact.get("Phone", ""), primaryContact.get("Fax", ""), customerID))

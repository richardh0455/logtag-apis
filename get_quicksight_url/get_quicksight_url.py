import boto3
import json
import os


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
    client = boto3.client('quicksight')
    dashboard_url = client.get_dashboard_embed_url(AwsAccountId="276219036989", DashboardId="48187bc4-17ee-4a2c-b474-e69e184bd270", IdentityType="IAM", SessionLifetimeInMinutes=100, ResetDisabled=True, UndoRedoDisabled=True)
    result = '{'
    result += 'URL:'
    result += dashboard_url
    result += '}'

    return done(result)

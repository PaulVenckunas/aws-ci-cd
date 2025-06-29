import os
# boto3 is aws-sdk for python
import boto3
import json


def handler(event, context):

    # Raw event data.
    # path = event["rawPath"]
    # if path != "/":
    #     return {"statusCode": 404, "body": "Not found."}

    # get a reference to the DDB table
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ.get("TABLE_NAME"))

    # Read the "VISIT COUNT" key (or create it if it doesnt exist)
    response = table.get_item(Key={"key": "visit_count"})
    if "Item" in response:
        visit_count = response["Item"]["value"]
    else:
        visit_count = 0

    #Increment the visit count and write it back to the table.
    new_visit_count = 1
    table.put_item(Item={"key": "visit_count", "value": new_visit_count})

    version = os.environ.get("VERSION", "0.0")
    response_body = {
        "message": "Hello World from Paul",
        "version": version
    }
    return {
        "statusCode": 200,
        "body": json.dumps(response_body),
        "headers": {
            "Content-Type": "application/json"
        }
    }
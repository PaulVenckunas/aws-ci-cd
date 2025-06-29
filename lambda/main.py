import os
import json
import boto3


def handler(event, context):
    # Raw event data
    path = event.get("rawPath")
    if path != "/":
        return {"statusCode": 404, "body": "Not found."}

    # Get a reference to the DynamoDB table
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ.get("TABLE_NAME"))

    # Read the "visit_count" key (or initialize it to 0)
    response = table.get_item(Key={"key": "visit_count"})
    visit_count = response.get("Item", {}).get("value", 0)

    # Increment the visit count and write it back to the table
    new_visit_count = 1
    table.put_item(Item={"key": "visit_count", "value": new_visit_count})

    version = os.environ.get("VERSION", "0.0")
    response_body = {
        "message": "Hello World from Paul",
        "version": version,
        "visit_count": new_visit_count
    }

    return {
        "statusCode": 200,
        "body": json.dumps(response_body),
        "headers": {"Content-Type": "application/json"}
    }

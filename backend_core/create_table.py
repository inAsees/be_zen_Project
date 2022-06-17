import os
import boto3
from dotenv import load_dotenv

load_dotenv()


def create_devices_table(dynamodb=None):
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    )
    # Table definition
    table = dynamodb.create_table(
        TableName='store_kewords',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                # AttributeType defines the data type. 'S' is string type and 'N' is number type
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            # ReadCapacityUnits set to 10 strongly consistent reads per second
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10  # WriteCapacityUnits set to 10 writes per second
        }
    )
    return table


if __name__ == '__main__':
    device_table = create_devices_table()
    # Print tablle status
    print("Status:", device_table.table_status)

# entry.py

import os
from flask_cors import CORS
import boto3

from flask import Flask, jsonify, request
app = Flask(__name__)
CORS(app)

CARDS_TABLE = os.environ['CARDS_TABLE']
client = boto3.client('dynamodb')


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/grocery/<string:item_name>")
def get_grocery(item_name):
    resp = client.get_item(
        TableName=CARDS_TABLE,
        Key={
            'itemName': { 'S': item_name }
        }
    )

    item = resp.get('Item')


    if not item:
        return jsonify({'error': 'User does not exist'}), 404


    return jsonify({
        'itemName': item.get('itemName').get('S'),
        'itemExpiration': item.get('itemExpiration').get('S'),
        'itemAmount': item.get('itemAmount').get('S')
    })


@app.route("/grocery", methods=["POST"])
def create_grocery():

    item_name = request.json.get('itemName')

    item_expiration = request.json.get('itemExpiration')
    
    item_amount = request.json.get("itemAmount")


    if not item_name or not item_expiration or not item_amount:
        return jsonify({'error': 'Please provide itemName, itemExpiration, and itemAmount'}), 400


    resp = client.put_item(
        TableName=CARDS_TABLE,
        Item={
            'itemName': {'S': item_name },
            'itemExpiration': {'S': item_expiration },
            'itemAmount': {'S': item_amount }
        }
    )

    return jsonify({
        'itemName': {'S': item_name },
        'itemExpiration': {'S': item_expiration },
        'itemAmount': {'S': item_amount }
    })



import json
import os
from datetime import datetime

import numpy as np

import ibm_boto3
import paho.mqtt.client as mqtt
from ibm_botocore.client import Config

# load credentials file
with open("credentials.json", "r") as read_file:
    credentials = json.load(read_file)

# name the bucket
bucket_name = 'alex-hw3-bucket'

# set up ibm_boto config and credentials
auth_endpoint = 'https://iam.bluemix.net/oidc/token'
service_endpoint = 'https://s3.private.us.cloud-object-storage.appdomain.cloud'

resource = ibm_boto3.resource(
    's3',
    ibm_api_key_id=credentials['apikey'],
    ibm_service_instance_id=credentials['resource_instance_id'],
    ibm_auth_endpoint=auth_endpoint,
    config=Config(signature_version='oauth'),
    endpoint_url=service_endpoint)

# Store IP address for broker
broker_ip = "169.59.1.50"
# Subscribe to all topics in image/capture
topic = "faces"
# choosing QoS 0 because I am in control of the pipeline end-to-end so there
# is little risk of data loss (and zero reprecussions if there is data loss)
qos_level = 0

# callback when connection occurs
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag=True
        client.subscribe(topic)
    print("connected: ", not bool(rc))


# callback for when message is received
def on_message(client, userdata, message):
    print("message received ")
    print("topic: ",message.topic)
    print("qos: ",message.qos)
    print("retain flag: ",message.retain)
    # generate unique timestamp for each image
    file_name = 'face_{}.png'.format(
        str(datetime.timestamp(datetime.now())).split('.')[0])
    msg = message.payload
    # Load data to bucket in COS
    resource.Bucket(name=bucket_name).put_object(Key=file_name, Body=msg)


# Initialize a client
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
# Connect to broker
client.connect(broker_ip)
# loop forever to grab all messages
client.loop_forever()

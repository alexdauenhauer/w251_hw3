import paho.mqtt.client as mqtt
# import ibm_boto3
from datetime import datetime
# import numpy as np
import os
# import json

# from ibm_botocore.client import Config 
# from time import gmtime, strftime



#Code adapted from https://cognitiveclass.ai/blog/read-and-write-csv-files-in-python-from-cloud/

#Saving credentials for bucket in a separate file and including a git ignore to protect identity
# with open("credentials.json", "r") as read_file:
#     credentials = json.load(read_file)

# updated
# bucket_name = 'hw3-bucket1'
save_path = '/mnt/mybucket'


# auth_endpoint = 'https://iam.bluemix.net/oidc/token'
# service_endpoint = 'https://s3.private.us.cloud-object-storage.appdomain.cloud'

# #Store relevant details for interacting with IBM COS store and uploading data
# resource = ibm_boto3.resource('s3',
#                       ibm_api_key_id=credentials['apikey'],
#                       ibm_service_instance_id=credentials['resource_instance_id'],
#                       ibm_auth_endpoint=auth_endpoint,
#                       config=Config(signature_version='oauth'),
#                       endpoint_url=service_endpoint)

#Code adapted from http://www.steves-internet-guide.com/publishing-messages-mqtt-client/
broker_address_sub = "169.59.1.50" #Store IP address for broker
# port = 1883 #Store port
topic_sub = "faces" #Subscribe to all topics in image/capture
qos_level = 0 #Set QOS level to 0 given connection is fairly stable and small amounts of data loss is tolerable

# #Initialize a counter to ensure unique image names
# count = 1

#Define what messages and actions to take when connecting.
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        client.subscribe(topic_sub) #Subscribe to topic
    print("connected: ", bool(rc))


#Define function for what to do when a message is received
def on_message(client, userdata, message):
    # global count #Access global variables
    print("message received ")
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    # currentTopic = message.topic #Store topic for formatted file names
    # datatype = currentTopic.split('/')[-1]
    # dateTime = strftime("%Y-%m-%d-%H-%M-%S", gmtime()) #Store date and time file came in
    # object_name = 'image_{}_{}_{}.png'.format(datatype,dateTime,count) #Set the file name
    file_name = 'face_{}.png'.format(
        str(datetime.timestamp(datetime.now())).split('.')[0])
    msg = message.payload #Grab the payload
    # resource.Bucket(name=bucket_name).put_object(Key=object_name, Body=msg)#Load data to bucket in COS
    # count +=1 #increment counter
    with open(os.path.join(save_path, file_name), 'w') as f:
        f.write(msg)


client_sub = mqtt.Client() #Initialize a client
client_sub.on_message = on_message #Use custom on message function
client_sub.on_connect = on_connect #Use custom on connect function
client_sub.connect(broker_address_sub) #Connect to broker
client_sub.loop_forever() #Ensure we can get all images that come through



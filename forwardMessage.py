import paho.mqtt.client as mqtt

# broker ip address
broker_ip = "172.20.0.2" 
# cloud ip address
cloud_ip = "169.59.1.50" 

# define the topic and QoS
topic_sub = "faces" 
qos_level = 0

# action to perform when connection occurs
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK Returned code=", rc)
	    client.subscribe(topic_sub)
    else:
        print("Bad connection Returned code=", rc)

# create function for callback
def on_publish(client,userdata,result):             
    print("data published to {}".format(topic))
    pass

# Define what to do when a subscribed message comes through
def on_message(client, userdata, message): 
    print("message received ")
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)

    msg = message.payload
    topic_pub = message.topic
    # Publish the message with its original topic and immediately forward the payload to the cloud
    # client_pub.publish(topic_pub, msg, qos=qos_level, retain=False)
    client.publish(topic_pub, msg, qos=qos_level, retain=False)

# Initialize the client for publishing to an external broker

cloud_pub = mqtt.Client("cloudForwardPub")
# Define custom message and function for when a subscribed message comes through
cloud_pub.on_message = on_message 
# Define custom on_publish message to ensure messages from both topics are being published
cloud_pub.on_publish = on_publish 
# Connect to cloud broker and keep connection alive
cloud_pub.connect(cloud_ip, keepalive=1200) 

# Initialize the client for subscribing to internal broker
broker_sub = mqtt.Client("cloudForwardSub") 
# Define custom message and function for when a subscribed message comes through
broker_sub.on_message = on_message
# Define custom on connect so that we subscribe to the topics locally
broker_sub.on_connect = on_connect 
# Define custom on_publish message to ensure messages from both topics are being
broker_sub.on_publish = on_publish 
# Connect to local broker
broker_sub.connect(broker_ip) 
# Keep loop running so that we continue to receive messages
broker_sub.loop_forever() 



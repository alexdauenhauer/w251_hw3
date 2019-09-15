# w251_hw3
## Project Summary

This project asked us to build a IoT application pipeline using a Jetson TX2 as the "edge" running through an MQTT broker-client pipeline to store captured images in the cloud.

In my MQTT pipeline I used QoS 0. I made this decision because it is the most minimal QoS level and part of the goal of this assignement was to remain lightweight. Since I had end-to-end control over the pipeline and there was no repurcussions if data was lost, QoS level 0 seemed appropriate since it will send a message once only and do nothing to guarantee receipt. I used a single MQTT topic and named it "faces" because it seemed like it fit with the theme of the assignment.

The faces can be located here:
http://s3.us.cloud-object-storage.appdomain.cloud\alex-hw3-bucket

some sample face captures are shown here

![face capture](face_1568064579.png?raw=true "Title")

![image on cloud](http://s3.us.cloud-object-storage.appdomain.cloud/alex-hw3-bucket/face_1568065554.png?raw=true "Title")

Here is a screencap of the data being saved in the bucket

![bucket](bucket.png?raw=true "Title")

## To make this all work
### Starting on the jetson side...
Build the dockerfiles you want. I made a dockerfile for the face detection, the MQTT broker and the MQTT forwarder
```sh
cd /path/to/Dockerfile
docker build -t myimage .
```
Once the dockerfiles are built, create a network to tie the broker and forwarder
```sh
docker network create --driver bridge hw03
```
Start up your broker. In my dockerfile I already downloaded the mosquitto packages so I only need to start up the broker
```sh
docker run --name mosquitto --network hw03 -p 1883:1883 -ti broker sh
# in the container now, spin up mosquitto broker
/usr/sbin/mosquitto
```
Leave this running, open a new terminal and spin up the forwarder container. Once inside, I run the `forwardMessage.py` script
```sh
docker run --name forwarder --network hw03 -ti forwarder sh
# inside the container, run the script
python3 forwardMessage.py
```
Now the broker and forwarder are listening and ready to receive messages and sent them to the cloud. Moving over to the cloud...
### In the cloud instance...
ssh to the cloud instance
```sh
ssh root@ip_of_vsi
```
build docker containers. I used the same broker container in the cloud as I did on the Jetson, I made a new one for the processor
```sh
cd /path/to/Dockerfile
docker build -t myimage .
```
build a docker network to tie the broker and processor together. Start up the broker, same way we did on the jetson
```sh
docker network create --driver bridge hw03
docker run --name mosquitto --network hw03 -p 1883:1883 -ti alpine sh
# now in the container run mosquitto
/usr/sbin/mosquitto
```
Leave this running, open a new terminal and spin up the processor container. Once inside, I run the `saveToBucket.py` script
```sh
docker run --name forwarder --network hw03 -ti processor sh
# now inside the container
python3 saveToBucket.py
```
Everything is now ready to extract faces. Back to the jetson
### Back in the jetson...
open up a new terminal and spin up the face dectection container. **NOTE:** need to run `xhost +` to allow the container to see the webcam device
```sh
xhost +
docker run -e DISPLAY=$DISPLAY --net=host --privileged -ti faces
```
Pick up the camera and point it at your face. Go to bucket and see that face images have magically been stored there

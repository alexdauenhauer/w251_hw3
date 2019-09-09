# w251_hw3

This project asked us to build a IoT application pipeline using a Jetson TX2 as the "edge" running through an MQTT broker-client pipeline to store captured images in the cloud.

In my MQTT pipeline I used QoS 0. I made this decision because it is the most minimal QoS level and part of the goal of this assignement was to remain lightweight. Since I had end-to-end control over the pipeline and there was no repurcussions if data was lost, QoS level 0 seemed appropriate since it will send a message once only and do nothing to guarantee receipt. I used a single MQTT topic and named it "faces" because it seemed like it fit with the theme of the assignment.

The faces can be located here:
s3.us.cloud-object-storage.appdomain.cloud\alex-hw3-bucket

some sample face captures are shown here
![face capture](face_1568064579.png?raw=true "Title")
![image on cloud](s3.us.cloud-object-storage.appdomain.cloud/alex-hw3-bucket/face_1568065554.png?raw=true "Title")

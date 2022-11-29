import rospy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import paho.mqtt.client as mqttClient
import time
import json
import sys

class connection():
    def __init__(self):
        Connected = False   #global variable for the state of the connection
        broker_address= "192.168.1.102"
        port = 1883
        self.client = mqttClient.Client("Python")               #create new instance
        self.client.on_connect = connection.on_connect                      #attach function to callback
        self.client.connect(broker_address, port=port)         #connect to broker
        self.client.loop_start()
        self.case_c = 0 


    def on_connect(client, userdata, flags, rc):
        if rc == 0:
        
            print("Connected to broker")
    
            global Connected                #Use global variable
            Connected = True                #Signal connection 
        else: 
            print("Connection failed")


    def pose_feed(self,pose_msg):
        pose_x = pose_msg.x
        pose_y = pose_msg.y
        MQTT_MSG=json.dumps({"brake":"1"})
        if self.case_c == 0:
                if pose_x <  0.55:
                    MQTT_MSG = json.dumps({"linear_x":"-1"})
                    print(pose_x,end="    forward\n")
                elif pose_x > 0.56:
                    MQTT_MSG = json.dumps({"brake":"1"})
                    print(pose_x,end="    brake\n")
                    self.case_c = 1
                self.client.publish("flipkart/bot3", MQTT_MSG)

        elif self.case_c == 1:
                if pose_x > 0.16:
                    MQTT_MSG = json.dumps({"linear_x":"1"})
                    print(pose_x,end="    backward\n")
                elif pose_x < 0.16:
                    MQTT_MSG = json.dumps({"brake":"1"})
                    print(pose_x,end="    brake\n")
                    self.case_c = 0
                self.client.publish("flipkart/bot3", MQTT_MSG)
    def stop_on_shutdown(self):
        MQTT_MSG = json.dumps({"brake":"1"})
        print("Terminated __ ||  ..")
        self.client.publish("flipkart/bot3", MQTT_MSG)


if __name__ == "__main__":

        cursor = connection()
        rospy.init_node("bot3_pose")
        data = rospy.Subscriber("/flipbot3/flipbot3/pose",Pose,cursor.pose_feed)
        rospy.spin()
        rospy.on_shutdown(cursor.stop_on_shutdown)
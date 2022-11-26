import rospy
from std_msgs.msg import String
from nav_msgs.msg import Odometry

class toAndFro():
    
    def __init__(self) :
        rospy.init_node("bot1_pose")
        rospy.Subscriber("/flipbot1/flipbot1/pose",Odometry,self.pose_feed)
        rospy.spin()

    def pose_feed(self,data):
        rospy.loginfo(data.data)


if __name__ == "__main__":
    obj = toAndFro()
    obj.pose_feed()
from morse.middleware.sockets.jointstate import fill_missing_pr2_joints

import roslib; roslib.load_manifest('sensor_msgs')
from sensor_msgs.msg import JointState

def init_extra_module(self, component_instance, function, mw_data):
    """ Setup the middleware connection with this data

    Prepare the middleware to handle the serialised data as necessary.
    """
    self.register_publisher(component_instance, function, JointState)

def _fill_jointstate(js, data):

    js.name = []
    js.position = []

    # collect name and positions of jointstates from sensor
    for k,v in data.items():
        js.name += v.keys()
        js.position += v.values()

    
    # for now leaving out velocity and effort
    #js.velocity = [1, 1, 1, 1, 1, 1, 1]
    #js.effort = [50, 50, 50, 50, 50, 50, 50]

def post_jointstate(self, component_instance):
    """
    Publish the data of an armature joint state as a ROS JointState
    """

    js = JointState()
    js.header = self.get_ros_header(component_instance)

    _fill_jointstate(js, component_instance.local_data)

    self.publish(js, component_instance)

def post_pr2_jointstate(self, component_instance):
    """
    Publish the data of an armature joint state as a ROS JointState
    """
    js = JointState()
    js.header = self.get_ros_header(component_instance)

    joints =  fill_missing_pr2_joints(component_instance.local_data)

    _fill_jointstate(js, {'joints': joints})

    self.publish(js, component_instance)
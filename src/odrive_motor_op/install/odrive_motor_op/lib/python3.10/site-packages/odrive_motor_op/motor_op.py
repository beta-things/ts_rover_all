import odrive 
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
import math
import time

class MotorOperation(Node):


    def __init__(self):
        super().__init__('motor_op')
        self.subscription = self.create_subscription(
            JointTrajectory,
            '/drives/joint_trajectory',
            self.trajectory_callback,
            10
        )
        
        self.get_logger().info(f'Motor opqqqqq start ')
        time.sleep(1) 
        self.odrv0 = odrive.find_any(serial_number = "386934673539") #FRONT RIGHT
        self.odrv1 = odrive.find_any(serial_number = "383934513539") #FRONT LEFT
        self.odrv2 = odrive.find_any(serial_number = "384934663539") #BACK RIGHT
        self.odrv3 = odrive.find_any(serial_number = "383C34583539") #BACK LEFT

        self.odrv0.axis0.requested_state = 8
        self.odrv1.axis0.requested_state = 8
        self.odrv2.axis0.requested_state = 8
        self.odrv3.axis0.requested_state = 8

        self.get_logger().info(f'Motor opZZZ running ')


    def trajectory_callback(self, msg):
        # msg.points[0].velocities[0] =  FRONT LEFT 
        # msg.points[0].velocities[1] = FRONT RIGHT 
        # msg.points[0].velocities[2]  = BACK LEFT 
        # msg.points[0].velocities[3] = BACK RIGHT 

        self.odrv0.axis0.controller.input_vel = (msg.points[0].velocities[1] / (2 * math.pi)) * 10         #FRONT RIGHT
        self.odrv1.axis0.controller.input_vel = (msg.points[0].velocities[2] / (2 * math.pi)) * 10   #FRONT LEFT
        self.odrv2.axis0.controller.input_vel = (msg.points[0].velocities[3] / (2 * math.pi)) * 10   #BACK RIGHT
        self.odrv3.axis0.controller.input_vel = (msg.points[0].velocities[0] / (2 * math.pi)) * 10 # * (-1)  #BACK LEFT
 

    def node_cleanup(self):
        self.get_logger().info('Node is shutting down...')
        # Your cleanup code here (if any)
        self.odrv0.axis0.requested_state = 1
        self.odrv1.axis0.requested_state = 1
        self.odrv2.axis0.requested_state = 1
        self.odrv3.axis0.requested_state = 1

def main(args=None):
    rclpy.init(args=args)
    motor_operation = MotorOperation()
    try:
        rclpy.spin(motor_operation)
    finally:
        motor_operation.node_cleanup()
        motor_operation.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()


# odr_all = odrive.connected_devices




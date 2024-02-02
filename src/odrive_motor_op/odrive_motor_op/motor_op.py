import odrive 
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory
from sensor_msgs.msg import JointState
import math
import time

class MotorOperation(Node):


    def __init__(self):
        super().__init__('motor_op')
        self.publisher_js = self.create_publisher(JointState, 'drives/joint_states', 10)
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

        # Timer setup to call a method (20 times per second)
        self.timer = self.create_timer(0.05, self.timer_callback)


    def trajectory_callback(self, msg):
        # msg.points[0].velocities[1] = FRONT RIGHT 
        # msg.points[0].velocities[0] =  FRONT LEFT 
        # msg.points[0].velocities[3] = BACK RIGHT 
        # msg.points[0].velocities[2]  = BACK LEFT 
        

        self.odrv0.axis0.controller.input_vel = (msg.points[0].velocities[1] / (2 * math.pi)) * 10         #FRONT RIGHT
        self.odrv1.axis0.controller.input_vel = (msg.points[0].velocities[0] / (2 * math.pi)) * 10 * (-1)  #FRONT LEFT
        self.odrv2.axis0.controller.input_vel = (msg.points[0].velocities[3] / (2 * math.pi)) * 10   #BACK RIGHT
        self.odrv3.axis0.controller.input_vel = (msg.points[0].velocities[2] / (2 * math.pi)) * 10 * (-1)  #BACK LEFT
 
       

    def timer_callback(self):
        # Code to be executed 20 times per second
        motorVel0 = (self.odrv0.axis0.pos_vel_mapper.vel/10)*(2*math.pi) #front right
        motorVel1 = ((self.odrv1.axis0.pos_vel_mapper.vel/10)*(-1))*(2*math.pi) #front left
        motorVel2 = (self.odrv2.axis0.pos_vel_mapper.vel/10)*(2*math.pi) #back right
        motorVel3 = ((self.odrv3.axis0.pos_vel_mapper.vel/10)*(-1))*(2*math.pi) #backLeft 
        # self.get_logger().info(f'Motor 3 vel :  {motorVel3}')

        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = ['mpo_500_wheel_front_left_joint', 'mpo_500_wheel_front_right_joint',  
        'mpo_500_wheel_back_left_joint','mpo_500_wheel_back_right_joint' ]
        joint_state.position = [0.0, 0.0, 0.0, 0.0]  # Replace with actual joint positions
        joint_state.velocity = [motorVel1, motorVel0, motorVel3, motorVel2]  # Replace with actual joint velocities
        joint_state.effort = [0.0, 0.0, 0.0, 0.0]    # Replace with actual joint efforts 

        self.publisher_js.publish(joint_state)

        pass

    def node_cleanup(self):
        self.get_logger().info('Node is shutting down...')
        # Your cleanup code here (if any)
        self.odrv0.clear_errors()
        self.odrv1.clear_errors()
        self.odrv2.clear_errors()
        self.odrv3.clear_errors()

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




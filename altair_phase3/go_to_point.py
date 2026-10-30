import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

TOLERANCE = 0.3      # arrival distance, turtlesim units
MAX_LINEAR = 1.5     # units/s
ANGLE_GAIN = 2.0
TURN_FIRST_RAD = 0.4  # turn in place if heading error is bigger than this


class GoToPoint(Node):
    def __init__(self):
        super().__init__('go_to_point')
        self.declare_parameter('target_x', 8.0)
        self.declare_parameter('target_y', 5.5)
        self.tx = self.get_parameter('target_x').value
        self.ty = self.get_parameter('target_y').value
        self.pose = None
        self.arrived = False
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 10)
        self.create_timer(0.1, self.tick)  # 10 Hz control loop
        self.get_logger().info(f'Heading to ({self.tx}, {self.ty})')

    def on_pose(self, msg):
        self.pose = msg

    def tick(self):
        if self.pose is None:
            return  # wait for the first pose before driving
        cmd = Twist()
        if not self.arrived:
            dx = self.tx - self.pose.x
            dy = self.ty - self.pose.y
            d = math.hypot(dx, dy)
            if d <= TOLERANCE:
                self.arrived = True
                self.get_logger().info(
                    f'ARRIVED at ({self.pose.x:.2f}, {self.pose.y:.2f}), d={d:.2f}')
            else:
                heading = math.atan2(dy, dx)
                delta = heading - self.pose.theta
                e = math.atan2(math.sin(delta), math.cos(delta))
                cmd.angular.z = ANGLE_GAIN * e
                if abs(e) > TURN_FIRST_RAD:
                    cmd.linear.x = 0.0
                else:
                    cmd.linear.x = min(MAX_LINEAR, 1.0 * d)
        self.cmd_pub.publish(cmd)  # zeros once arrived


def main():
    rclpy.init()
    node = GoToPoint()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()

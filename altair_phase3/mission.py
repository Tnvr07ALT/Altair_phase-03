import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool
from std_srvs.srv import Trigger
from turtlesim.msg import Pose

TOLERANCE = 0.3       # arrival distance, turtlesim units
MAX_LINEAR = 0.5      # units/s, slow enough to interrupt on camera
ANGLE_GAIN = 2.0
TURN_FIRST_RAD = 0.4  # turn in place if heading error is bigger than this

RUNNING = 'RUNNING'
PAUSED = 'PAUSED'
DONE = 'DONE'


class Mission(Node):
    def __init__(self):
        super().__init__('mission')
        # Waypoints are parameters so one coordinate can be changed on camera.
        defaults = [('bottle', 8.0, 5.5), ('mallet', 8.0, 8.0), ('base', 5.5, 5.5)]
        self.targets = []
        for name, x, y in defaults:
            self.declare_parameter(f'{name}_x', x)
            self.declare_parameter(f'{name}_y', y)
            self.targets.append((
                name.capitalize(),
                self.get_parameter(f'{name}_x').value,
                self.get_parameter(f'{name}_y').value))

        self.target_idx = 0
        self.state = RUNNING
        self.blocked = False   # latest /field_blocked flag, clear at start
        self.pose = None

        # This node is the ONLY publisher of /turtle1/cmd_vel.
        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 10)
        self.create_subscription(Bool, '/field_blocked', self.on_blocked, 10)
        self.create_service(Trigger, '/resume_mission', self.on_resume)
        self.create_timer(0.1, self.tick)  # 10 Hz control loop

        route = ' -> '.join(f'{n}({x},{y})' for n, x, y in self.targets)
        self.get_logger().info(f'Mission route: {route}')

    def on_pose(self, msg):
        self.pose = msg

    def on_blocked(self, msg):
        self.blocked = msg.data
        if self.blocked:
            if self.state == RUNNING:
                self.state = PAUSED
                name = self.targets[self.target_idx][0]
                self.get_logger().warn(f'BLOCKED: PAUSED while heading to {name}')
            else:
                self.get_logger().info(f'Blocked report received (state {self.state})')
        else:
            # A clear report does NOT change self.state. Only on_resume can
            # move PAUSED back to RUNNING, so there is no automatic resume.
            self.get_logger().info(
                f'Block report cleared. State stays {self.state}; '
                'call /resume_mission to continue.')

    def on_resume(self, request, response):
        if self.pose is None:
            response.success = False
            response.message = 'Rejected: no pose received yet'
        elif self.state == DONE:
            response.success = False
            response.message = 'Rejected: mission already complete'
        elif self.state == RUNNING:
            response.success = False
            response.message = 'Rejected: mission is already running'
        elif self.blocked:
            response.success = False
            response.message = 'Rejected: route is still blocked'
        else:
            self.state = RUNNING
            response.success = True
            response.message = f'Resumed: heading to {self.targets[self.target_idx][0]}'
        self.get_logger().info(f'Resume request: {response.message}')
        return response

    def tick(self):
        if self.pose is None:
            return  # wait for the first pose before driving
        cmd = Twist()  # zero velocity unless we decide to move
        if self.state == RUNNING:
            name, tx, ty = self.targets[self.target_idx]
            dx = tx - self.pose.x
            dy = ty - self.pose.y
            d = math.hypot(dx, dy)
            if d <= TOLERANCE:
                self.get_logger().info(
                    f'ARRIVED at {name} ({self.pose.x:.2f}, {self.pose.y:.2f}), d={d:.2f}')
                self.target_idx += 1
                if self.target_idx >= len(self.targets):
                    self.state = DONE
                    self.get_logger().info('DONE')
            else:
                heading = math.atan2(dy, dx)
                delta = heading - self.pose.theta
                e = math.atan2(math.sin(delta), math.cos(delta))
                cmd.angular.z = ANGLE_GAIN * e
                if abs(e) <= TURN_FIRST_RAD:
                    cmd.linear.x = min(MAX_LINEAR, 1.0 * d)
        # PAUSED and DONE fall through here: zero velocity every tick.
        self.cmd_pub.publish(cmd)


def main():
    rclpy.init()
    node = Mission()
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

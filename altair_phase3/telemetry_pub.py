import json
import math
import time

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MarsTelemetryPublisher(Node):
    def __init__(self):
        super().__init__('mars_telemetry_publisher')
        self.declare_parameter('start_battery_pct', 30.0)
        self.declare_parameter('depletion_pct_per_s', 1.0)
        self.start_battery = self.get_parameter('start_battery_pct').value
        self.depletion = self.get_parameter('depletion_pct_per_s').value
        self.pub = self.create_publisher(String, 'rover/telemetry', 10)
        self.t0 = time.monotonic()
        self.timer = self.create_timer(1.0, self.tick)  # 1 Hz
        self.get_logger().info(
            f'Publishing on /rover/telemetry, start battery '
            f'{self.start_battery}%, depletion {self.depletion} %/s')

    def tick(self):
        elapsed = time.monotonic() - self.t0
        battery = max(0.0, self.start_battery - self.depletion * elapsed)
        wheel_speed = 0.5 + 0.3 * math.sin(elapsed / 3.0)
        temperature = min(70.0, 25.0 + 0.4 * elapsed + 0.5 * math.sin(elapsed))
        reading = {
            'battery_pct': round(battery, 1),
            'temperature_c': round(temperature, 1),
            'wheel_speed_mps': round(wheel_speed, 2),
            'elapsed_s': round(elapsed, 1),
        }
        msg = String()
        msg.data = json.dumps(reading)
        self.pub.publish(msg)


def main():
    rclpy.init()
    node = MarsTelemetryPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()

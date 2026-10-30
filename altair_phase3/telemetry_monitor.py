import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

LOW_BATTERY_PCT = 25.0


class MissionControlMonitor(Node):
    def __init__(self):
        super().__init__('mission_control_monitor')
        self.sub = self.create_subscription(
            String, 'rover/telemetry', self.on_telemetry, 10)

    def on_telemetry(self, msg):
        try:
            r = json.loads(msg.data)
            battery = r['battery_pct']
        except (json.JSONDecodeError, KeyError):
            self.get_logger().error(f'Bad telemetry message: {msg.data}')
            return
        self.get_logger().info(
            f"t={r['elapsed_s']:.0f}s | battery {battery:.1f}% | "
            f"temp {r['temperature_c']:.1f} C | "
            f"wheel {r['wheel_speed_mps']:.2f} m/s")
        if battery < LOW_BATTERY_PCT:
            self.get_logger().warn(
                f'LOW BATTERY: {battery:.1f}% (below {LOW_BATTERY_PCT:.0f}%)')


def main():
    rclpy.init()
    node = MissionControlMonitor()
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

import math
import queue
import threading
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

TURN = 1.0  # rad/s, so a turn of X radians takes X seconds

# Each segment: (linear.x in units/s, angular.z in rad/s, duration in s)
PATTERNS = {
    'P': [(1.0, 0.0, 3.0), (0.0, TURN, math.pi), (1.0, 0.0, 3.0)],
    'R': [(1.0, 0.0, 3.0), (0.0, TURN, math.pi / 2),
          (1.0, 0.0, 1.5), (0.0, TURN, math.pi / 2),
          (1.0, 0.0, 3.0), (0.0, TURN, math.pi / 2),
          (1.0, 0.0, 1.5), (0.0, TURN, math.pi / 2)],
    'Z': [(1.0, 0.0, 1.5), (0.0, TURN, math.pi / 3),
          (1.0, 0.0, 1.5), (0.0, -TURN, 2 * math.pi / 3),
          (1.0, 0.0, 1.5)],
}
NAMES = {'P': 'Patrol', 'R': 'Rectangle', 'Z': 'Zigzag'}


class DriveMenu(Node):
    def __init__(self):
        context = rclpy.get_default_context()
        super().__init__('drive_menu', context=context)
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.cmds = queue.Queue()
        self.ready = threading.Event()
        self.ready.set()
        self.quit = False
        self.segments = None
        self.idx = 0
        self.seg_start = 0.0
        
        # Background thread for keyboard input
        threading.Thread(target=self.read_input, daemon=True).start()
        self.timer = self.create_timer(0.02, self.tick)  # 50 Hz

    def read_input(self):
        while True:
            self.ready.wait()
            self.ready.clear()
            try:
                text = input('\nCommand  P=Patrol  R=Rectangle  Z=Zigzag  Q=Quit : ')
            except EOFError:
                text = 'Q'
            self.cmds.put(text)

    def send(self, lin, ang):
        msg = Twist()
        msg.linear.x = float(lin)
        msg.angular.z = float(ang)
        self.pub.publish(msg)

    def stop(self):
        self.send(0.0, 0.0)

    def handle_command(self, text):
        key = text.strip().upper()
        if key in PATTERNS:
            print(f'Running {NAMES[key]}...')
            self.segments = PATTERNS[key]
            self.idx = 0
            self.seg_start = time.monotonic()
        elif key == 'Q':
            print('Stopping and quitting.')
            self.stop()
            self.quit = True
        else:
            print(f'Invalid input "{text}". Use P, R, Z or Q.')
            self.ready.set()

    def tick(self):
        if self.segments is None:
            try:
                text = self.cmds.get_nowait()
            except queue.Empty:
                return
            self.handle_command(text)
            return

        now = time.monotonic()
        lin, ang, dur = self.segments[self.idx]
        if now - self.seg_start >= dur:
            self.seg_start += dur
            self.idx += 1
            if self.idx >= len(self.segments):
                self.stop()
                self.segments = None
                print('Pattern finished.')
                self.ready.set()
                return
            lin, ang, dur = self.segments[self.idx]
        self.send(lin, ang)


def main(args=None):
    rclpy.init(args=args)
    try:
        node = DriveMenu()
        while rclpy.ok() and not node.quit:
            rclpy.spin_once(node, timeout_sec=0.1)
        node.stop()
        node.destroy_node()
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == '__main__':
    main()

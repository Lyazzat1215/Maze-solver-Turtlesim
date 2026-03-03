import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math


class Maze_Solver(Node):

    def __init__(self):
        super().__init__('maze_solver_node')

        self.cmd_pub = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.pose_sub = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self.pose = None
        self.state = "MOVE_FORWARD"
        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info("Maze Solver Node Started")

    def pose_callback(self, msg):
        self.pose = msg
    def control_loop(self):
        if self.pose is None:
            return

        cmd = Twist()
        margin = 1.0
        near_wall = (
            self.pose.x < margin or
            self.pose.x > 11 - margin or
            self.pose.y < margin or
            self.pose.y > 11 - margin
        )

        if self.state == "MOVE_FORWARD":

            if near_wall:
                self.get_logger().info("Wall detected. Switching to TURN state.")
                self.state = "TURN"
            else:
                cmd.linear.x = 2.0
                cmd.angular.z = 0.0

        elif self.state == "TURN":
            cmd.linear.x = 0.0
            cmd.angular.z = 2.0

            # Когда угол примерно кратен 90°, возвращаемся к движению
            if abs(self.pose.theta % (math.pi / 2)) < 0.1:
                self.get_logger().info("Turn completed. Moving forward.")
                self.state = "MOVE_FORWARD"
        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = MazeSolver()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
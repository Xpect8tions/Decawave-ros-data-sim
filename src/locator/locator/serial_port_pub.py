from std_msgs.msg import String
import rclpy
from rclpy.node import Node

#####################################
node_name = "math_pub"
#####################################


class RangingPub(Node):
    def __init__(self):
        super().__init__(node_name)
        self.get_logger().info(f"initalised node: {node_name}")
        self.publish_ = self.create_publisher(String, '/output', 1)
        self.create_timer(1, self.publish)
        self.x = 1.423
        self.y = 1.234
        self.z = 2.134
        self.incre = 0.05

    def publish(self):
        while (True):
            msg = String()
            msg.data = f'''
5478[0.50,0.50,1.97] 2479[5.02,0.50,1.97] 4248[5.02,3.50,1.97] f678[0.50,3.50,1.97] le_us=5423 est[{self.x},{self.y},{self.z},94]
'''
            self.publish_.publish(msg)
            self.get_logger().info(f'published: {msg}')
            self.x += self.incre
            self.y += self.incre
            self.incre += 0.001
            break
# 5478[0.50,0.50,1.97]


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = RangingPub()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

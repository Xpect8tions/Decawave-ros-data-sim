# region imports
import subprocess
import datetime
import time 
import numpy as np
from datetime import datetime
from re import sub

from std_msgs.msg import String
import rclpy
import rclpy.time
from rclpy.node import Node
from visualization_msgs.msg import Marker

# endregion

# region global data
################################
Node_name = "serial_sub"
################################
Path_to_log = "src/locator/logging/DWranging.csv"
print(f"opening {Path_to_log} to append only")
Dwm_logger = open(Path_to_log, "a+")
################################
Max_anchors = 4
Topic = "/output"  # change depending on the actual topic name
################################
# endregion
subprocess.run(["get","topic","info"],shell=True,capture_output= True,text=True)
class RangingSub(Node):
    def __init__(self):
        super().__init__(Node_name)
        self.get_logger().info(f"initalised node: {Node_name}")
        self.declare_parameters(
            namespace="",
            parameters=[
                ("anchor_id", ['-99']),
            ],
        )
        self.get_logger().info("declared parameters:")
        self.anchor_list = self.get_parameter("anchor_id").value
        self.get_logger().info(f"anchor_id = {self.anchor_list}")

        self.get_logger().info(f"creating subscription to {Topic} topic")
        self.sub1 = self.create_subscription(String, Topic, self.subscriber, 1)
        self.last_proc_list = []
        
        self.Rviz_pubber = self.create_publisher(Marker, "marker_msgs", 10)
        self.pub = self.create_timer(1 / 10, self.rviz_pub)
        self.last_list = []
        self.has_msg = False

    def subscriber(self, msg):
        if msg:
            self.has_msg = True
        else:
            self.has_msg = False
            self.get_logger().info('no msg')
        if self.has_msg:
            self.time = datetime.now()
            self.get_logger().info('subscriber start')
            write_list = [self.time]
            data = msg.data
            data_list = data.split(' ')
            self.get_logger().info(f'data_list = {data_list}')
            good_list = []
            item = 0
            for info in data_list:
                if '\n' in info:
                    info = info.replace('\n', '')
                good_list.append(str(info))
                item +=1
            self.get_logger().info(f'good_list = {good_list}')
            full_list = []
            self.some_list = []

            for itm in good_list:
                if '[' in itm:
                    itm = itm.replace('[',',')
                    itm = itm.replace(']','')
                elif 'le_us=' in itm:
                    itm = itm.replace('le_us=','')
                elif 'est' in itm:
                    itm = itm.replace('est','')
                self.get_logger().info(f'itm = {itm}')
                half_list = itm.split(',')
                self.get_logger().info(f'half_list = {half_list}')
                self.some_list.append(half_list)
            count = 0
            for some in self.some_list:
                self.get_logger().info(f'count = {count}')
                self.get_logger().info(f'some = {some}')
                if len(some) == 1:
                    store = some[0]
                    self.some_list[count+1].remove('est')
                    self.some_list[count+1].insert(0,store)
                    self.get_logger().info(f'self.some_list[count+1] = {self.some_list[count+1]}')
                    self.some_list.remove(some)
                count += 1

                for i in half_list:
                    if i != 'est':
                        full_list.append(i)
            self.get_logger().info(f'somelist = {self.some_list}')
            self.get_logger().info(f'full_list = {full_list}')
            for strng in full_list:
                write_list.append(strng)
            str_time = str(self.time)
            if self.last_list == []:
                vel = -9.9
                self.get_logger().info('vel = -9.9')
                self.last_time = str_time
                self.get_logger().info(f'last_time = {self.last_time}')
            else:
                x1 = float(full_list[len(full_list)-3])
                y1 = float(full_list[len(full_list)-2])
                z1 = float(full_list[len(full_list)-1])
                calc_list = [x1,y1,z1]
                self.get_logger().info(f'calc_list = {calc_list}')

                x2 = float(self.last_list[len(self.last_list)-3])
                y2 = float(self.last_list[len(self.last_list)-2])
                z2 = float(self.last_list[len(self.last_list)-1])
                last_list_calc = [x2,y2,z2]
                self.get_logger().info(f'last_list_calc = {last_list_calc}')
                distance = np.sqrt(((x1 - x2)**2)+((y1 - y2)**2)+((z1 - z2)**2))
                self.get_logger().info(f'distance = {distance}')

                math_last_time = datetime.strptime(self.last_time, "%Y-%m-%d %H:%M:%S.%f")
                math_time = datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S.%f")
                time_diff = math_time - math_last_time
                time_diff_math = time_diff.total_seconds()
                self.get_logger().info(f'time_diff_math = {time_diff_math}')
                vel = distance/time_diff_math
                self.get_logger().info(f'vel = {vel}')
            self.last_list = full_list
            write_list.append(vel)
            write = "\n"
            for info in write_list:
                write = f"{write}{info}, "
            self.get_logger().info(f'write = {write}')
            Dwm_logger.write(write)
        self.get_logger().info(f'subscriber end')

    def rviz_pub(self):
        self.get_logger().info(f"marker_pub start")
        if self.has_msg:
            for item in self.some_list:
                self.get_logger().info(f"item = {item}")
                msg = Marker()
                ts_time = str(self.time.timestamp())
                self.get_logger().info(f'ts_time = {ts_time}')
                ts_lis = ts_time.split('.')
                msg.header.stamp.sec = int(ts_lis[0])
                msg.header.stamp.nanosec = int(ts_lis[1])
                msg.header.frame_id = "map"
                msg.id = int(f'{item[0]}',16)
                msg.type = 3
                msg.action = 0
                msg.lifetime.sec = 0
                msg.pose.position.x = float(item[1])
                msg.pose.position.y = float(item[2])
                msg.pose.position.z = float(item[3])
                for anc in self.anchor_list:
                    self.get_logger().info(f'anc = {anc}')
                    if anc == item[0]:
                        msg.color.r = 1.0
                        msg.color.g = 0.0
                        msg.color.b = 0.0
                        msg.color.a = 1.0
                        msg.scale.x = 1.0
                        msg.scale.y = 1.0
                        msg.scale.z = 1.0
                        break
                    else:
                        msg.color.r = 0.0
                        msg.color.g = 0.0
                        msg.color.b = 1.0
                        msg.color.a = 1.0
                        msg.scale.x = 1.0
                        msg.scale.y = 1.0
                        msg.scale.z = 1.0
                self.Rviz_pubber.publish(msg)
                # self.get_logger().info(f'published {msg}')
            time.sleep(1/30)
        self.has_msg = False
        self.get_logger().info(f"marker_pub end")

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = RangingSub()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

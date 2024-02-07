# /locator

This folder contains the files where the publisher and subscriber nodes are created. It also stores the csv files that will store the UWB log data.

## serial_port_pub

[serial_port_pub.py](./locator/serial_port_pub.py) creates a publisher that publishes a string message to the `/output` message. The message simulates a moving UWB tag and the 4 anchors that can detect the tag.

the information published to the topic are as such:

| ID   | type   | Location (x,y,z)          |
| ---- | ------ | ------------------------- |
| 5478 | anchor | 0.50,0.50,1.97            |
| 2479 | anchor | 5.02,0.50,1.97            |
| 4248 | anchor | 5.02,3.50,1.97            |
| f678 | anchor | 0.50,3.50,1.97            |
| 5423 | tag    | 1.423,1.234,2.134 (start) |

## serial_port_sub

[serial_port_sub.py](./locator/serial_port_sub.py) creates a subscriber to the `/output` topic and processes it before saving the recieved data in [DWranging.csv](./logging/DWranging.csv). The csv stores the location and ids of the anchors and tags, along with the quality

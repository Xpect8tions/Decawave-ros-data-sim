# /config folder

## rviz_config.rviz

This file is read by RViz when it gets launched by [serial.launch.py](../launch/serial.launch.py) replace this file if you wish to use a different config.

the default values in the file are as such:

| Fixed frame | Topic      |
| ----------- | ---------- |
| 'map'       | '/markers' |

## serial_params.yaml

This yaml parameters file contains a list of names of the UWB anchors. update this file if you wish to test different names and/or numbers of UWBs.

import time
import numpy as np
from pop import Util
from pop import LiDAR
from pop.Util import imshow
import threading

class LiDARManager:
    def __init__(self):
        self.lidar = LiDAR.Rplidar()
        self.lidar.connect()
        self.lidar.startMotor()
        self.lidar_map = None
        self.lidar_map_lock = threading.Lock()
        self.stop_event = threading.Event()

    def __del__(self):
        self.lidar.stopMotor()


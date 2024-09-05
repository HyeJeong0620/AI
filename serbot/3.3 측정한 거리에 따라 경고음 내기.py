import time
import numpy as np
from pop import LiDAR
from pop import Pilot
from pop.Util import imshow
import threading
import pyaudio

class LiDARManager:
    def __int__(self):
        self.lidar = LiDAR.Rplidar()
        self.lidar_map = None
        self.lidar_map_lock = threading.Lock()
        self.stop_event = threading.Event()
        self.distTh = 1000
        self.minDist = 1000

    def get_map_thread(self):
        while not self.stop_event.is_set():
            local_map = self.lidar.getMap(limit_distance = 3000, size(300, 300))
            with self.lidar_map_lock:
                self.lidar_map = local_map
            time.sleep(0.03)
        print('thread getMap terminated')

    def check_distance_thread(self):
        bot = Pilot.Serbot()
        while not self.stop_event.is_set():
            vectors = self.lidar.getVertors()

            flag = False
            mindDist
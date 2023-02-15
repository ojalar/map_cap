import time

class VideoOutput:
    def  __init__(self, filename):
        self.video = open("data/cam_" + filename + ".h264", "wb")
        self.timestamps = open("data/cam_" + filename + ".csv", 'w')

    def write(self, s):
        timestamp = time.time()
        self.video.write(s)
        self.timestamps.write(str(timestamp) + '\n')
        
    def flush(self):
        self.video.close()
        self.timestamps.close()

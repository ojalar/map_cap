import time

class VideoOutput:
    def  __init__(self, filename):
        self.video = open(filename + ".h264", "wb")
        self.timestamps = open(current_time + ".csv", 'w')

    def write(self, s):
        timestamp = time.time()
        self.video.write(s)
        self.timestamps.write(str(timestamp) + '\n')
        
    def flush(self):
        self.video.close()
        self.timestamps.close()

import time

# custom output for recording video from the Raspberry Pi camera
class VideoOutput:
    def  __init__(self, filename):
        # open files for writing video and timestamp data
        self.video = open("data/cam_" + filename + ".h264", "wb")
        self.timestamps = open("data/cam_" + filename + ".csv", 'w')

    def write(self, s):
        # write frame and timestamp in respective files
        timestamp = time.time()
        self.video.write(s)
        self.timestamps.write(str(timestamp) + '\n')
        
    def flush(self):
        # close files
        self.video.close()
        self.timestamps.close()

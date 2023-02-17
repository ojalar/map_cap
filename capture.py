import time
import RPi.GPIO as GPIO
from picamera import PiCamera
from video import VideoOutput
from imu import IMU
import traceback

# main class for recording with the camera unit
class Recorder:
    def __init__(self):
        # pin numbers on the Raspi GPIO for the led and button
        self.ledpin = 5
        self.buttonpin = 6

        # camera setup
        self.cam = PiCamera()
        self.cam.resolution = (1640, 1232)
        self.cam.framerate = 10

        # imu setup
        self.imu = IMU()

        # recording state, changed with the button
        # 0 for waiting
        # 1 for recording
        self.state = 0

        # GPIO setup for led and button
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ledpin, GPIO.OUT)
        GPIO.setup(self.buttonpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # add interrupt to button push for changing state
        GPIO.add_event_detect(self.buttonpin, GPIO.FALLING, 
            callback = self.change_state, bouncetime = 1000)
    
        # indicate successful initialisation
        self.blink(3)

    def capture(self):
        # capture data from the camera and imu
        while True:
            # only initiate recording if state is appropriate
            if self.state == 1:
                timestamp = str(int(time.time()))
                self.cam.start_recording(VideoOutput(timestamp), format="h264")
                self.imu.start_recording(timestamp)
                while self.state == 1:
                    self.imu.log()
                    
                self.cam.stop_recording()
                self.imu.stop_recording()
            


    def change_state(self, channel):
        # change the recording state, initiated by button interrupt
        self.state = 1 - self.state
        # change led state accordingly, led is lit during recording
        if self.state == 1:
            GPIO.output(self.ledpin, GPIO.HIGH)
        else:
            GPIO.output(self.ledpin, GPIO.LOW) 

    def blink(self, n):
        # blink led n times
        GPIO.output(self.ledpin, GPIO.LOW)
        time.sleep(0.5)
        for i in range(n):
            GPIO.output(self.ledpin, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(self.ledpin, GPIO.LOW)
            time.sleep(0.5)
        # return led to correct state 
        if self.state == 1:
            GPIO.output(self.ledpin, GPIO.HIGH)
        else:
            GPIO.output(self.ledpin, GPIO.LOW) 


if __name__ == "__main__":
    try:
        recorder = Recorder()
        recorder.capture()
    except:
        print(traceback.format_exc())
        GPIO.cleanup()

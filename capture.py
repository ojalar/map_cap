import time
import RPi.GPIO as GPIO

class Recorder:
    def __init__(self):
        # pin numbers on the Raspi GPIO
        self.ledpin = 5
        self.buttonpin = 6
        # fps to use for recording
        self.fps = 10

        # recording state
        self.state = 0

        # GPIO setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.ledpin, GPIO.OUT)
        GPIO.setup(self.buttonpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.buttonpin, GPIO.FALLING, 
            callback = self.change_state, bouncetime = 100)
    
        # indicate successful initialisation
        self.blink(3)

    def capture(self):
        # capture data
        pass
            


    def change_state(self):
        # change the recording state
        self.state = 1 - self.state
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
        while True:
            pass
    except:
        GPIO.cleanup()

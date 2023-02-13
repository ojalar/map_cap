from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import smbus
import time

class IMU:
    def __init__(self, calib_path = None):
        self.imu = MPU9250(
            address_ak=AK8963_ADDRESS, 
            address_mpu_master=MPU9050_ADDRESS_68, # In 0x68 Address
            address_mpu_slave=None, 
            bus=1,
            gfs=GFS_1000, 
            afs=AFS_8G, 
            mfs=AK8963_BIT_16, 
            mode=AK8963_MODE_C100HZ)
        
        self.imu.configure()

        self.f = None

        if calib_path != None:
            self.imu.abias = [0, 0, 0] # Set the master accelerometer biases
            self.gyro.abias = [0, 0, 0]
            self.imu.magScale = [0, 0, 0]  
            self.imu.mbias = [0, 0, 0] # Set magnetometer hard iron distortion
    
    def log(self):
        timestamp = time.time()
        data = self.imu.getAllData()
        
    def calibrate(self):
        self.imu.calibrate()
        self.imu.configure()
    
    def start_recording(filename):
        self.f = open(filename, 'w')

    def stop_recording():
        self.f.close()

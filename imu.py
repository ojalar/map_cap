from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import time
import numpy as np

# class for recording data from the MPU9250 imu
class IMU:
    def __init__(self, calib_path = None):
        # initialise imu 
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
        
        # file variable for logging data
        self.f = None
        
        # initialise calibration data if provided
        if calib_path != None:
            data = np.loadtxt(calib_path, delimiter = ',')
            self.imu.abias = data[0, :] 
            self.imu.gbias = data[1, :]
            self.imu.magScale = data[2, :]  
            self.imu.mbias = data[3, :]
    
    def log(self):
        # function for logging the imu readings to a file
        data = self.imu.getAllData()
        data = [str(x) for x in data]
        self.f.write(','.join(data) + '\n')

    def calibrate(self):
        # function for calibrating the imu.
        # imu has to be stationary, and gravity in z-axis direction
        self.imu.calibrate()
        self.imu.configure()
        # reformat the calibration results and write in file
        abias = [str(x) for x in self.imu.abias] 
        gbias = [str(x) for x in self.imu.gbias]
        mscale = [str(x) for x in self.imu.magScale]
        mbias = [str(x) for x in self.imu.mbias]
        with open("calib/imu.csv", 'w') as c:
            c.write(','.join(abias) + '\n')
            c.write(','.join(gbias) + '\n')
            c.write(','.join(mscale) + '\n')
            c.write(','.join(mbias))

    def start_recording(self, filename):
        # function for initialising recording
        # open file for data logging
        self.f = open("data/imu_" + filename + ".csv", 'w')
        
    def stop_recording(self):
        # stop recording cleanly
        # close the file used for logging
        self.f.close()

    def generate_header(self):
        # convenience function for generating the header
        # for the logged data format
        with open("data/header.csv", 'w') as h:
            labels = self.imu.getAllDataLabels()
            h.write(','.join(labels))


if __name__ == "__main__":
    imu = IMU("calib/imu.csv")
    imu.calibrate()
    #imu.start_recording("test")
    #imu.log()
    #imu.log()
    #imu.stop_recording()
    #imu.generate_header()

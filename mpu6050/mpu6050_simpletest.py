from concurrent.futures import thread
import time
import board
import adafruit_mpu6050
import math
# import numpy as np
from statistics import mean
import lcd_display
import threading
class MPU_6050():
    def __init__(self) -> None:
        i2c = board.I2C()  # uses board.SCL and board.SDA
        self.mpu = adafruit_mpu6050.MPU6050(i2c)
        self.v_x = 0
        self.v_y = 0
        self.v_z = 0
        self.axlist = []
        self.aylist = []

    def calculate_velocity(self, cur_vel, new_a, pattent_time):
        return cur_vel + (time.time() - pattent_time)* new_a

    def execute_class(self):
        count = 0
        while True:
            a_x, a_y, a_z = self.mpu.acceleration
            start_time = time.time()
            if len(self.axlist)<30:
                # self.axlist.pop(0)
                # self.aylist.pop(0)
                self.axlist.append(a_x)
                self.aylist.append(a_y)
            time.sleep(0.01)
            # self.v_x = self.calculate_velocity(self.v_x, a_x- mean(self.axlist), start_time)
            # self.v_y = self.calculate_velocity(self.v_y, a_y- mean(self.aylist), start_time)
            # self.v_z = self.calculate_velocity(self.v_z, a_z, start_time)
            # velocity_message = 'Velocity = ' + str(round(math.sqrt(self.v_x*self.v_x + self.v_y*self.v_y ),1))
            # print(math.sqrt(self.v_x*self.v_x + self.v_y*self.v_y ))
            # lcd_display.LCD_display(velocity_message, 1, 1)
            # print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (self.mpu.acceleration))
            # print("Gyro X:%.2f, Y: %.2f, Z: %.2f rad/s" % (mpu.gyro))
            #print("Temperature: %.2f C" % mpu.temperature)
            # print("")
            # time.sleep(0.1)
            a_x_diff = a_x- mean(self.axlist)
            a_y_diff = a_y- mean(self.aylist)
            if a_x_diff > 0.1 or a_y_diff > 0.1:
                message = 'Ha Cho an khu'
                # message = f'{round(a_x_diff,2)}, {round(a_y- mean(self.aylist),2)}'
                print(message)
                # if int(time.time()%60) - int(start_time%60) == 1:
                count += 1
                if count > 5:
                    threading.Thread(target=lcd_display.LCD_display, args=(message, 1, 0)).start()
                    count = 0
            else: 
                count = 0
mpu = MPU_6050()
mpu.execute_class()

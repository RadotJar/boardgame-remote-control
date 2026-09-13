import sys
import tty
import termios
import select
import time
import board
import busio

from gpiozero import OutputDevice
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

class Laser:
    LASER_GPIO = 17
    PAN_CHANNEL = 0
    PAN_MIN = 20
    PAN_MAX = 160
    TILT_CHANNEL = 1
    TILT_MIN = 30
    TILT_MAX = 150
    STEP = 2

    def __init__(self):
        self.laser = OutputDevice(
            Laser.LASER_GPIO,
            active_high=True,
            initial_value=False
        )

        self.i2c = busio.I2C(board.SCL, board.SDA)

        self.pca = PCA9685(self.i2c)
        self.pca.frequency = 50

        self.pan = servo.Servo(
            self.pca.channels[Laser.PAN_CHANNEL],
            min_pulse=500,
            max_pulse=2400
        )

        self.tilt = servo.Servo(
            self.pca.channels[Laser.TILT_CHANNEL],
            min_pulse=500,
            max_pulse=2400
        )

        self.pan_angle = 90
        self.tilt_angle = 90
        self.laser_on = False

        self.pan.angle = self.pan_angle
        self.tilt.angle = self.tilt_angle

    def teardown(self):
        # Laser OFF
        self.laser.off()
        self.laser.close()
    
        # Release servos
        self.pca.channels[Laser.PAN_CHANNEL].duty_cycle = 0
        self.pca.channels[Laser.TILT_CHANNEL].duty_cycle = 0
    
        self.pca.deinit()
    
        print("\nShutdown cleanly")

    def handle_key_press(self, key):
        if key == "w":
            self.tilt_angle = max(
                Laser.TILT_MIN,
                self.tilt_angle - Laser.STEP
            )

        elif key == "s":
            self.tilt_angle = min(
                Laser.TILT_MAX,
                self.tilt_angle + Laser.STEP
            )

        elif key == "a":
            self.pan_angle = max(
                Laser.PAN_MIN,
                self.pan_angle - Laser.STEP
            )

        elif key == "d":
            self.pan_angle = min(
                Laser.PAN_MAX,
                self.pan_angle + Laser.STEP
            )

        elif key == " ":
            self.laser_on = not self.laser_on

            if laser_on:
                laser.on()
            else:
                laser.off()

        elif key == "c":
            self.pan_angle = 90
            self.tilt_angle = 90

        elif key == "q":
            return

        self.pan.angle = self.pan_angle
        self.tilt.angle = self.tilt_angle
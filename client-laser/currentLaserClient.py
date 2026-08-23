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


# -------------------------
# Configuration
# -------------------------

LASER_GPIO = 17

PAN_CHANNEL = 0
TILT_CHANNEL = 1

PAN_MIN = 20
PAN_MAX = 160

TILT_MIN = 30
TILT_MAX = 150

STEP = 2


# -------------------------
# Hardware setup
# -------------------------

laser = OutputDevice(
    LASER_GPIO,
    active_high=True,
    initial_value=False
)

i2c = busio.I2C(board.SCL, board.SDA)

pca = PCA9685(i2c)
pca.frequency = 50

pan = servo.Servo(
    pca.channels[PAN_CHANNEL],
    min_pulse=500,
    max_pulse=2400
)

tilt = servo.Servo(
    pca.channels[TILT_CHANNEL],
    min_pulse=500,
    max_pulse=2400
)


# -------------------------
# Initial state
# -------------------------

pan_angle = 90
tilt_angle = 90
laser_on = False

pan.angle = pan_angle
tilt.angle = tilt_angle


# -------------------------
# Keyboard
# -------------------------

old_settings = termios.tcgetattr(sys.stdin)

print("""
W/S     Tilt
A/D     Pan
SPACE   Toggle laser
C       Centre
Q       Quit

No Enter required.
""")


try:
    tty.setcbreak(sys.stdin.fileno())

    while True:

        # Wait briefly for a key
        if select.select([sys.stdin], [], [], 0.05)[0]:
            key = sys.stdin.read(1).lower()

            if key == "w":
                tilt_angle = max(
                    TILT_MIN,
                    tilt_angle - STEP
                )

            elif key == "s":
                tilt_angle = min(
                    TILT_MAX,
                    tilt_angle + STEP
                )

            elif key == "a":
                pan_angle = max(
                    PAN_MIN,
                    pan_angle - STEP
                )

            elif key == "d":
                pan_angle = min(
                    PAN_MAX,
                    pan_angle + STEP
                )

            elif key == " ":
                laser_on = not laser_on

                if laser_on:
                    laser.on()
                else:
                    laser.off()

            elif key == "c":
                pan_angle = 90
                tilt_angle = 90

            elif key == "q":
                break

            pan.angle = pan_angle
            tilt.angle = tilt_angle

            print(
                f"\rPan: {pan_angle:3d}° | "
                f"Tilt: {tilt_angle:3d}° | "
                f"Laser: {'ON ' if laser_on else 'OFF'}",
                end="",
                flush=True
            )

        time.sleep(0.01)


finally:

    # Restore terminal
    termios.tcsetattr(
        sys.stdin,
        termios.TCSADRAIN,
        old_settings
    )

    # Laser OFF
    laser.off()
    laser.close()

    # Release servos
    pca.channels[PAN_CHANNEL].duty_cycle = 0
    pca.channels[TILT_CHANNEL].duty_cycle = 0

    pca.deinit()

    print("\nShutdown cleanly")
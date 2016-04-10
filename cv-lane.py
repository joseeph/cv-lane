from cv.EyeCanSee import *
from ai.pid import *
from controller.controllers import *

import cv2
import math
import time
import cv.settings

# Our class instances
camera = EyeCanSee()

# PID for each region (if we do decide to add any)
pid = {}
for region in settings.REGIONS_KEYS:
    pid[region] = PID(p=.35, i=.125, d=.305, integrator_max=10, integrator_min=-10)

motor = MotorController() # values: -100 <= x <= 100
steering = ServoController() # values: 0 <= x <= 100

motor.run_speed(20)

for i in range(0, 125):
    # Trys and get our lane
    camera.where_lane_be()

    # Pid on each region
    total_pid = 0
    for region in camera.relative_error:
        total_pid += pid[region].update(camera.relative_error[region])
    # Negative total_pid = need to turn left
    # Positive total_pid = need to turn right
    # Try to keep pid 0
    if total_pid < 0:
        if total_pid < -100:
            total_pid = -100
        steering.turn_left(abs(total_pid))

    elif total_pid > 0:
        if total_pid > 100:
            total_pid = 100
        steering.turn_right(abs(total_pid))

    time.sleep(0.01)

motor.run_speed(-25)

time.sleep(2.5)

steering.straighten()
motor.stop()
import math
from vex import *

# ------------------ CONSTANTS ------------------
TRACK_WIDTH_MM = 300
DEFAULT_SPEED = 60

# ------------------ LOW-LEVEL ARC DRIVER ------------------
def drive_arc(ds_mm, radius_mm, speed_pct=DEFAULT_SPEED):
    """
    Drives a very small arc segment.
    """
    left_dist  = ds_mm * (radius_mm - TRACK_WIDTH_MM / 2) / radius_mm
    right_dist = ds_mm * (radius_mm + TRACK_WIDTH_MM / 2) / radius_mm

    left_dist.spin_for(FORWARD, left_dist, MM, velocity=speed_pct, wait=False)
    right_dist.spin_for(FORWARD, right_dist, MM, velocity=speed_pct)

# ------------------ PARABOLIC PATH ------------------
# y = a x^2
def drive_parabola(a=0.002, x_max=500, steps=100, speed_pct=DEFAULT_SPEED):
    dx = x_max / steps
    x = 0

    for _ in range(steps):
        dy_dx = 2 * a * x
        d2y_dx2 = 2 * a

        R = ((1 + dy_dx**2) ** 1.5) / abs(d2y_dx2)
        ds = math.sqrt(dx**2 + (dy_dx * dx)**2)

        drive_arc(ds, R, speed_pct)
        x += dx

# ------------------ ELLIPTICAL PATH ------------------
# x = a cos(t), y = b sin(t)
def drive_ellipse(a=400, b=250, steps=150, speed_pct=DEFAULT_SPEED):
    dt = (2 * math.pi) / steps
    t = 0

    for _ in range(steps):
        dx = -a * math.sin(t) * dt
        dy =  b * math.cos(t) * dt

        ds = math.sqrt(dx*dx + dy*dy)
        R = abs((a * b) / ((b * math.cos(t))**2 + (a * math.sin(t))**2)**1.5)

        drive_arc(ds, R, speed_pct)
        t += dt

# ------------------ HYPERBOLIC PATH ------------------
# x = a cosh(t), y = b sinh(t)
def drive_hyperbola(a=200, b=150, t_max=1.5, steps=120, speed_pct=DEFAULT_SPEED):
    dt = t_max / steps
    t = 0

    for _ in range(steps):
        dx = a * math.sinh(t) * dt
        dy = b * math.cosh(t) * dt

        ds = math.sqrt(dx*dx + dy*dy)
        R = abs((a * b) / ((b * math.cosh(t))**2 + (a * math.sinh(t))**2)**1.5)

        drive_arc(ds, R, speed_pct)
        t += dt



from vex import *
import math

brain=Brain()
L=Motor(Ports.PORT1,GearSetting.RATIO_18_1,False)
R=Motor(Ports.PORT10,GearSetting.RATIO_18_1,True)
W=0.3;dt=0.02;t=0

while t<40:
    # --- Circle ---
    if t<6.28:
        x=lambda s:1*math.cos(s);y=lambda s:1*math.sin(s)
        dx=lambda s:-1*math.sin(s);dy=lambda s:1*math.cos(s)
        ddx=lambda s:-1*math.cos(s);ddy=lambda s:-1*math.sin(s)
        s=t
    # --- Ellipse ---
    elif t<12.56:
        a,b=1.2,0.6
        x=lambda s:a*math.cos(s);y=lambda s:b*math.sin(s)
        dx=lambda s:-a*math.sin(s);dy=lambda s:b*math.cos(s)
        ddx=lambda s:-a*math.cos(s);ddy=lambda s:-b*math.sin(s)
        s=t-6.28
    # --- Parabola ---
    elif t<18:
        x=lambda s:s;y=lambda s:s**2
        dx=lambda s:1;dy=lambda s:2*s
        ddx=lambda s:0;ddy=lambda s:2
        s=t-12.56
    # --- Hyperbola ---
    elif t<24:
        a,b=0.5,0.5
        x=lambda s:a*math.cosh(s);y=lambda s:b*math.sinh(s)
        dx=lambda s:a*math.sinh(s);dy=lambda s:b*math.cosh(s)
        ddx=lambda s:a*math.cosh(s);ddy=lambda s:b*math.sinh(s)
        s=t-18
    # --- Degenerate: pair of lines (x=y, x=-y) ---
    elif t<30:
        x=lambda s:s;y=lambda s:s
        dx=lambda s:1;dy=lambda s:1
        ddx=lambda s:0;ddy=lambda s:0
        s=t-24
    else:
        x=lambda s:s;y=lambda s:-s
        dx=lambda s:1;dy=lambda s:-1
        ddx=lambda s:0;ddy=lambda s:0
        s=t-30

    vx=dx(s);vy=dy(s);ax=ddx(s);ay=ddy(s)
    v=(vx*vx+vy*vy)**0.5
    k=(vx*ay-vy*ax)/((vx*vx+vy*vy)**1.5) if v!=0 else 0
    w=v*k
    L.spin(FORWARD,(v-(W/2)*w)*120,RPM)
    R.spin(FORWARD,(v+(W/2)*w)*120,RPM)
    wait(dt,SECONDS)
    t+=dt

from vex import *
import math

brain = Brain()
L = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
R = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True)
W = 0.3; dt = 0.02; t = 0

# cumulative integrals
int_x = 0
int_y = 0

while t < 40:
    # --- choose conic section ---
    if t < 6.28:  # circle
        f_x = lambda s: math.cos(s)
        f_y = lambda s: math.sin(s)
        s = t
    elif t < 12.56:  # ellipse
        a,b = 1.2,0.6
        f_x = lambda s: a*math.cos(s)
        f_y = lambda s: b*math.sin(s)
        s = t-6.28
    elif t < 18:  # parabola
        f_x = lambda s: 1
        f_y = lambda s: 2*s
        s = t-12.56
    elif t < 24:  # hyperbola
        a,b = 0.5,0.5
        f_x = lambda s: a*math.cosh(s)
        f_y = lambda s: b*math.sinh(s)
        s = t-18
    elif t < 30:  # line x=y
        f_x = lambda s: 1
        f_y = lambda s: 1
        s = t-24
    else:  # line x=-y
        f_x = lambda s: 1
        f_y = lambda s: -1
        s = t-30

    # --- integrals ---
    int_x += f_x(s)*dt
    int_y += f_y(s)*dt

    # --- derivatives of integrals (just original functions) ---
    vx = f_x(s)
    vy = f_y(s)

    # --- second derivatives for curvature (numerical derivative of original functions) ---
    ax = (f_x(s+dt)-f_x(s))/dt
    ay = (f_y(s+dt)-f_y(s))/dt

    v = math.sqrt(vx*vx + vy*vy)
    k = (vx*ay - vy*ax)/((vx*vx + vy*vy)**1.5) if v != 0 else 0
    w = v*k

    # --- wheel velocities using derivatives and integral positions ---
    L.spin(FORWARD, (v-(W/2)*w)*120, RPM)
    R.spin(FORWARD, (v+(W/2)*w)*120, RPM)

    t += dt
    wait(dt, SECONDS)


from vex import *

# initializing the important stuff
brain = Brain()
controller = Controller()

# pneumatic
match_load = Pneumatics(brain.three_wire_port.c)

# descore
descore = Pneumatics(brain.three_wire_port.f)

# motors
right1 = Motor(Ports.PORT2, False)
right2 = Motor(Ports.PORT11, False)
right3 = Motor(Ports.PORT1, True)
left1 = Motor(Ports.PORT10, False)
left2 = Motor(Ports.PORT9, True)
left3 = Motor(Ports.PORT20, True)

# intake
intake = Motor(Ports.PORT8, True)

# outtake
# flip True/False here if direction feels wrong
outtake = Motor(Ports.PORT3, False)

# motorgroups
left = MotorGroup(left1, left2, left3)
right = MotorGroup(right1, right2, right3)

# inertial
inertial = Inertial(Ports.PORT5)

# Smartdrive for auton (still available if you want it)
drivetrain = SmartDrive(left, right, inertial)

######################################################################################################
# Scale input function
######################################################################################################

def scale_input(x):
    return (x * abs(x)) / 100

######################################################################################################
# Fast rate limiter function
######################################################################################################

def slow_rate_limit(current_speed, target_speed, step=10):
    if target_speed > current_speed + step:
        return current_speed + step
    elif target_speed < current_speed - step:
        return current_speed - step
    else:
        return target_speed

######################################################################################################
# PID controller class
######################################################################################################

class PID:
    def __init__(self, kP, kI, kD, integral_limit=100):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.integral_limit = integral_limit

        self.error = 0
        self.prev_error = 0
        self.integral = 0
        self.derivative = 0

    def calculate(self, target, current):
        self.error = target - current

        # integral with anti-windup
        self.integral += self.error
        if abs(self.integral) > self.integral_limit:
            self.integral = self.integral_limit * (1 if self.integral > 0 else -1)

        self.derivative = self.error - self.prev_error
        self.prev_error = self.error

        return (self.error * self.kP) + (self.integral * self.kI) + (self.derivative * self.kD)

    def reset(self):
        self.error = 0
        self.prev_error = 0
        self.integral = 0
        self.derivative = 0

######################################################################################################
# PID drive straight (distance in mm)
######################################################################################################

def drive_pid(distance_mm, speed_cap=80):
    # approximate wheel circumference in mm (adjust if needed)
    wheel_circ = 320
    target_deg = (distance_mm / wheel_circ) * 360

    left1.set_position(0, DEGREES)
    right1.set_position(0, DEGREES)

    pid = PID(kP=0.35, kI=0.0, kD=0.2)

    while True:
        left_pos = left1.position(DEGREES)
        right_pos = right1.position(DEGREES)
        avg_pos = (left_pos + right_pos) / 2

        power = pid.calculate(target_deg, avg_pos)

        # cap speed
        if power > speed_cap:
            power = speed_cap
        if power < -speed_cap:
            power = -speed_cap

        left.spin(FORWARD, power, PERCENT)
        right.spin(FORWARD, power, PERCENT)

        # exit condition
        if abs(pid.error) < 5:
            break

        wait(20, MSEC)

    left.stop(BRAKE)
    right.stop(BRAKE)

######################################################################################################
# PID turn to heading (degrees 0–360)
######################################################################################################

def turn_pid(target_heading, speed_cap=60):
    # make sure inertial is calibrated before auton
    pid = PID(kP=0.6, kI=0.0, kD=0.25)

    while True:
        current = inertial.heading()
        # shortest path wrap-around
        error = target_heading - current
        if error > 180:
            current += 360
        elif error < -180:
            current -= 360

        power = pid.calculate(target_heading, current)

        if power > speed_cap:
            power = speed_cap
        if power < -speed_cap:
            power = -speed_cap

        left.spin(FORWARD, power, PERCENT)
        right.spin(REVERSE, power, PERCENT)

        if abs(pid.error) < 1.5:
            break

        wait(20, MSEC)

    left.stop(BRAKE)
    right.stop(BRAKE)

######################################################################################################
# Driver control
######################################################################################################

def driver_control():
    lastpressed = False
    last_pressed_2 = False
    togle = False
    toggle_2 = False
    left_actual = 0
    right_actual = 0

    while True:
        forw = controller.axis3.position()
        tur = controller.axis1.position() * 0.72

        if -5 < forw < 5:
            forw = 0
        if -5 < tur < 5:
            tur = 0

        forward = scale_input(forw)
        turn = scale_input(tur)

        left_target = forward + turn
        right_target = forward - turn

        left_actual = slow_rate_limit(left_actual, left_target, step=20)
        right_actual = slow_rate_limit(right_actual, right_target, step=20)

        left.spin(DirectionType.FORWARD, left_actual, VelocityUnits.PERCENT)
        right.spin(DirectionType.FORWARD, right_actual, VelocityUnits.PERCENT)

        # intake
        if controller.buttonR1.pressing():
            intake.spin(FORWARD, 100, PERCENT)
        elif controller.buttonL1.pressing():
            intake.spin(REVERSE, 100, PERCENT)
        else:
            intake.stop()

        # outtake
        if controller.buttonRight.pressing():
            outtake.spin(FORWARD, 100, PERCENT)
        elif controller.buttonA.pressing():
            outtake.spin(REVERSE, 100, PERCENT)
        else:
            outtake.stop()

        # match load pneumatic
        if lastpressed == False and controller.buttonB.pressing():
            togle = not togle
            if togle:
                match_load.open()
            else:
                match_load.close()
        lastpressed = controller.buttonB.pressing()

        # descore pneumatic
        if controller.buttonDown.pressing() and last_pressed_2 == False:
            toggle_2 = not toggle_2
            if toggle_2:
                descore.open()
            else:
                descore.close()
        last_pressed_2 = controller.buttonDown.pressing()

        wait(50, MSEC)

######################################################################################################
# Auton (left side) using PID
######################################################################################################

def auton_leftLong():
    # make sure inertial is calibrated before running this in real match
    inertial.calibrate()
    while inertial.is_calibrating():
        wait(20, MSEC)

    # drive forward to first position
    drive_pid(556)

    # turn left ~90 degrees
    turn_pid(90)

    # small reverse
    drive_pid(-100)

    wait(100, MSEC)
    match_load.open()

    # slower approach
    drive_pid(240)

    intake.spin(FORWARD, 100, PERCENT)
    wait(1500, MSEC)
    intake.stop()

    # tiny heading correction if needed (optional)
    # turn_pid(91)

    # back up to scoring spot
    drive_pid(-476)

    intake.spin(FORWARD, 100, PERCENT)
    outtake.spin(REVERSE, 100, PERCENT)
    wait(4000, MSEC)
    intake.stop()
    outtake.stop()

def auton_rightLong():
    # Ensure inertial is calibrated
    inertial.calibrate()
    while inertial.is_calibrating():
        wait(20, MSEC)

    # Start intake and drive forward to first ball
    intake.spin(FORWARD, 100, PERCENT)
    drive_pid(514)   # was drivetrain.drive_for(FORWARD, 514, MM)
    wait(500, MSEC)
    intake.stop()

    wait(100, MSEC)

    # Turn left 66 degrees
    turn_pid(66)

    # Drive forward to intake next ball
    drive_pid(125)

    # Reverse intake to score
    intake.spin(REVERSE, 85, PERCENT)
    wait(2500, MSEC)
    intake.stop()

    wait(50, MSEC)

    # Intake forward while backing up
    intake.spin(FORWARD, 100, PERCENT)
    drive_pid(-654)
    intake.stop()

    # Turn left 145 degrees
    turn_pid(145)

    wait(200, MSEC)
    match_load.open()

    wait(200, MSEC)

    # Drive forward to match load position
    drive_pid(300)

    wait(1000, MSEC)

    # Back up
    drive_pid(-550)

    # Score balls
    intake.spin(FORWARD, 100, PERCENT)
    outtake.spin(FORWARD, 100, PERCENT)
    wait(2000, MSEC)
    intake.stop()
    outtake.stop()

######################################################################################################
# Competition setup
######################################################################################################

Competition(driver_control, auton_leftLong)

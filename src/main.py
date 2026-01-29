from vex import *

#intitializing the important stuff
brain = Brain()
controller = Controller()

#pneumatic
match_load = Pneumatics(brain.three_wire_port.c)

#desco
descore = Pneumatics(brain.three_wire_port.f)

#motors
right1 = Motor(Ports.PORT2, False)
right2 = Motor(Ports.PORT11, False)
right3 = Motor(Ports.PORT1, True)
left1 = Motor(Ports.PORT10, False)
left2 = Motor(Ports.PORT9, True)
left3 = Motor(Ports.PORT20, True)

#intake
intake = Motor(Ports.PORT8, True)

#outake
outtake = Motor(Ports.PORT3, False)

#motorgroups
left = MotorGroup(left1, left2, left3)
right = MotorGroup(right1, right2, right3)
inouttake = MotorGroup(intake, outtake)

#inertial
inertial = Inertial(Ports.PORT5)

# Smartdrive for auton
drivetrain = SmartDrive(left, right, inertial)

######################################################################################################
# Scale input function
# This takes the joystick input (x) and applies a parabolic scaling, 
# except the from -infinity to 0, the outputs are negative to allow robot to turn back.
# Instead of a linear response, it squares the input (keeping the sign),
# which makes small joystick movements more precise while still allowing
# full speed when holding the joystick all the way.
# Example: input 50 → (50 * abs(50)) / 100 = 25
######################################################################################################

def scale_input(x):
    return (x * abs(x)) / 100 
######################################################################################################
# Fast rate limiter function
# This prevents the motor speed from changing too abruptly.
# It gradually steps the current speed(the value of this can be seen later in the driver control)
# toward the target speed (the value can also be seen later)
# by a fixed increment, or step, which is by default = 5. This smooths acceleration/deceleration
# so the robot doesn't jerk  when the joystick changes suddenly.
######################################################################################################

def slow_rate_limit(current_speed, target_speed, step=10):
    if target_speed > current_speed + step:
        return current_speed + step
    elif target_speed < current_speed - step:
        return current_speed - step
    else:
        return target_speed

#  the most important function
def driver_control(): 

    # Track button state and motor speeds
    lastpressed = False  # state toggle (i think??)
    last_pressed_2 = False
    togle = False  # toggle on or off pneumatics
    toggle_2 = False
    left_actual = 0  # set default speed of left motors at start
    right_actual = 0  # set default speed of right motors at start


    while True:
        forw = controller.axis3.position() # forward/backward joystick
        tur = controller.axis1.position() * 0.72 # right/left joystick

        # Deadzone filtering - wont move when the joystick is barely pressed
        if -5 < forw < 5:
            forw = 0
        if -5 < tur < 5:
            tur = 0

        # Apply parabolic scaling from earlier
        forward = scale_input(forw)
        turn = scale_input(tur)

        # combine forward + turn
        left_target = forward + turn
        right_target = forward - turn

        # Apply slow limiter for smooth decel
        # Slow rate limiter:
        # This function prevents the motors from instantly jumping to the target speed.
        # Instead, it gradually moves the current speed toward the target in fixed steps.
        #
        # Why? Joystick inputs can change very suddenly (e.g., from 0% to 100% in a fast rate).
        # If motors followed that instantly, the robot would jump forward, skid, or stress
        # its mechanical parts. The limiter smooths this out so the robot feels more controlled.
        #
        # How it works:
        # - If target speed is higher than current, increase by 'step'.
        # - If target speed is lower, decrease by 'step'.
        # - If target is within 'step' range, snap directly to target.
        #
        # Example:
        #   current = 20, target = 50, step = 5 → next = 25
        #   current = 25, target = 50, step = 5 → next = 30
        #   ... continues until current reaches 50.
        #
        # Effect: acceleration and deceleration happen smoothly over several cycles,
        # making the robot easier to drive precisely, safely and protects hardware.
        left_actual = slow_rate_limit(left_actual, left_target, step=20)
        right_actual = slow_rate_limit(right_actual, right_target, step=20)

        left.spin(DirectionType.FORWARD, left_actual, VelocityUnits.PERCENT) 
        right.spin(DirectionType.FORWARD, right_actual, VelocityUnits.PERCENT)
#cp???
    
        #0.35 torque according to internet
        if controller.buttonR1.pressing():
            intake.spin(FORWARD, 100, PERCENT)
        elif controller.buttonL1.pressing():
            intake.spin(REVERSE, 100, PERCENT)
        else:
            intake.stop()
        
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

        if controller.buttonDown.pressing() and last_pressed_2 == False:
            toggle_2 = not toggle_2
            if toggle_2:
                descore.open()
            else:
                descore.close()
        last_pressed_2 = controller.buttonDown.pressing()

        wait(50)

#auton for later
def auton_rightLong():
    # might have to set velocity later
    intake.spin(FORWARD, 100, PERCENT)
    drivetrain.drive_for(FORWARD, 454, MM) # maybe 528
    wait(800, MSEC) 
    intake.stop()
    wait(100, MSEC)
    drivetrain.turn_for(LEFT, 52, DEGREES)           
    drivetrain.drive_for(FORWARD, 139, MM)
    intake.spin(REVERSE, 85, PERCENT)
    wait(2500, MSEC)
    intake.stop()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    wait(50, MSEC)
    intake.spin(FORWARD, 100, PERCENT)
    drivetrain.drive_for(REVERSE, 654, MM)
    intake.stop() 
    drivetrain.turn_for(LEFT, 145, DEGREES)
    wait(200, MSEC)
    match_load.open()
    intake.spin(FORWARD, 100, PERCENT)
    drivetrain.set_drive_velocity(85, RPM)
    wait(200, MSEC)
    drivetrain.drive_for(FORWARD, 300, MM) 
    wait(1500, MSEC)
    intake.stop()
    drivetrain.drive_for(REVERSE, 550, MM)
    intake.spin(FORWARD, 100, PERCENT)
    outtake.spin(REVERSE, 100, PERCENT)
    wait(4000, MSEC)
    intake.stop()
    outtake.stop() 

def auton_leftLong():
    drivetrain.drive_for(FORWARD, 556, MM)
    drivetrain.turn_for(LEFT, 90, DEGREES)
    drivetrain.drive_for(REVERSE, 100, MM)
    wait(100, MSEC)
    match_load.open()
    drivetrain.set_drive_velocity(75, RPM)
    wait(500, MSEC)
    intake.spin(FORWARD, 150, PERCENT)
    drivetrain.drive_for(FORWARD, 240, MM)
    wait(1500, MSEC)
    intake.stop()
    drivetrain.turn_for(RIGHT, 1, DEGREES)
    drivetrain.drive_for(REVERSE, 476, MM)
    intake.spin(FORWARD, 100, PERCENT)
    outtake.spin(REVERSE, 100, PERCENT)
    wait(4000, MSEC)
    intake.stop()
    outtake.stop() 



def testauton():
    pass

def Julie_auton():
    intake.spin(FORWARD, 100, PERCENT)
    drivetrain.drive_for(FORWARD, 600, MM)
    intake.stop()
    wait(100)
    drivetrain.turn_for(LEFT, 90, DEGREES)
    drivetrain.drive_for(FORWARD, 25, MM)
    intake.spin(REVERSE, 100, PERCENT)
    wait(100)
    drivetrain.drive_for(REVERSE, 600, MM)
    drivetrain.turn_for(LEFT, 180, DEGREES)
    wait(100)
    intake.spin(FORWARD, 100, PERCENT)
    drivetrain.drive_for(FORWARD, 60, MM)
    intake.stop()
    drivetrain.turn_for(RIGHT, 45, DEGREES)
    drivetrain.drive_for(FORWARD, 200, MM)
    wait(100)
    drivetrain.turn_for(LEFT, 270, DEGREES)
    drivetrain.drive_for(FORWARD, 180, MM)
    intake.spin(FORWARD, 100, PERCENT)
    intake.stop()
    wait(100)
    drivetrain.drive_for(REVERSE, 180, MM)
    inouttake.spin(FORWARD, 100, PERCENT)
    drivetrain.turn_for(RIGHT, 90, DEGREES)
    drivetrain.drive_for(FORWARD, 800, MM)
    wait(100)
    drivetrain.turn_for(RIGHT, 90, DEGREES)
    drivetrain.drive_for(FORWARD, 80, MM)
    intake.spin(FORWARD, 100, PERCENT)
    intake.stop()
    wait(100)
    drivetrain.drive_for(REVERSE, 250, MM)
    intake.spin(FORWARD, 100, PERCENT)
    intake.stop()
    drivetrain.drive_for(REVERSE, 20, MM)
    drivetrain.turn_for(LEFT, 180, DEGREES)
    wait(100)
    drivetrain.drive_for(FORWARD, 200, MM)
    wait(100)

def auton_skill():
    # might have to set velocity later
    intake.spin(FORWARD, 100, PERCENT)
    drivetrain.drive_for(FORWARD, 502, MM) # maybe 528
    wait(500, MSEC) 
    intake.stop()
    wait(100, MSEC)
    drivetrain.turn_for(LEFT, 68, DEGREES)           
    drivetrain.drive_for(FORWARD, 135, MM)
    intake.spin(REVERSE, 85, PERCENT)
    wait(2500, MSEC)
    intake.stop()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
    wait(50, MSEC)
    drivetrain.drive_for(REVERSE, 654, MM) 
    drivetrain.turn_for(LEFT, 140, DEGREES)
    wait(200, MSEC)
    match_load.open()
    intake.spin(FORWARD, 100, PERCENT)
    drivetrain.set_drive_velocity(85, RPM)
    wait(200, MSEC)
    drivetrain.drive_for(FORWARD, 400, MM)
    wait(2000, MSEC)
    intake.stop()
    wait(20, MSEC)
    drivetrain.drive_for(REVERSE, 600, MM)
    intake.spin(FORWARD, 100, PERCENT)
    outtake.spin(REVERSE, 100, PERCENT)
    wait(1500, MSEC)
    intake.stop()
    outtake.stop()
    wait(50,MSEC)
    drivetrain.turn_for(RIGHT, 12, DEGREES)
    drivetrain.drive_for(FORWARD, 1000, MM)
    drivetrain.turn_for(LEFT, 66, DEGREES)
    drivetrain.drive_for(REVERSE, 100, MM)
    match_load.open()
    drivetrain.drive_for(FORWARD, 250, MM)
    intake.spin(FORWARD, 100, PERCENT)
    wait(2000, MSEC)
    intake.stop()
    drivetrain.drive_for(REVERSE, 460, MM)
    intake.spin(FORWARD, 100, PERCENT)
    outtake.spin(FORWARD, 100, PERCENT)
    wait(2000, MSEC)
    intake.stop()
    outtake.stop()
    drivetrain.turn_for(LEFT, 72, DEGREES)
    drivetrain.drive_for(FORWARD, 500, MM)



Competition(driver_control, auton_rightLong)

#robotics is cool sometimes
#idk
#i dont like band
#i like cp i watched chris paul play basketball



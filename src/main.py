from vex import *
#import math

#intitializing the important stuff
brain = Brain()
controller = Controller()

#pneumatic
match_load = Pneumatics(Ports.PORT1)

#motors
right1 = Motor(Ports.PORT3, False)
right2 = Motor(Ports.PORT2, False)
right3 = Motor(Ports.PORT1, False)
left1 = Motor(Ports.PORT9, True)
left2 = Motor(Ports.PORT7, True)
left3 = Motor(Ports.PORT6, True)

#intake
intake_1= Motor(Ports.PORT17, True)
intake_2 = Motor(Ports.PORT10, True)

#motorgroups
left = MotorGroup(left1, left2, left3)
right = MotorGroup(right1, right2, right3)
intake = MotorGroup(intake_1, intake_2)

#inertial
inertial = Inertial(Ports.PORT15)

# Smartdrive for auton
drivetrain = SmartDrive(left,right, inertial)

# for jinwoong to look at
'''
######################################################################################################
# Scale input function
# This takes the joystick input (x) and applies a parabolic scaling, 
# except the from -infinity to 0, the outputs are negative to allow robot to turn back.
# Instead of a linear response, it squares the input (keeping the sign),
# which makes small joystick movements more precise while still allowing
# full speed when holding the joystick all the way.
# Example: input 50 → (50 * abs(50)) / 100 = 25
######################################################################################################

#def scale_input(x):
    #return (x * abs(x)) / 100 
######################################################################################################
# Fast rate limiter function
# This prevents the motor speed from changing too abruptly.
# It gradually steps the current speed(the value of this can be seen later in the driver control)
# toward the target speed (the value can also be seen later)
# by a fixed increment, or step, which is by default = 5. This smooths acceleration/deceleration
# so the robot doesn't jerk  when the joystick changes suddenly.
######################################################################################################

def fast_rate_limit(current_speed, target_speed, step=5):
    if target_speed > current_speed + step:
        return current_speed + step
    elif target_speed < current_speed - step:
        return current_speed - step
    else:
        return target_speed

'''

#  the most important function
def driver_control(): 
    #for jinwoong to look at
    '''
    # Track button state and motor speeds
    lastpressed = False  # state toggle (i think??)
    spining = False  # toggle on or off pneumatics
    left_actual = 0  # set default speed of left motors at start
    right_actual = 0  # cset default speed of right motors at start


    while True:
        forw = controller.axis3.position() # forward/backward joystick
        tur = controller.axis1.position() # right/left joystick

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
        left_actual = slow_rate_limit(left_actual, left_target, step=5)
        right_actual = slow_rate_limit(right_actual, right_target, step=5)
        left_actual = slow_rate_limit(left_actual, left_target, step=5)
        right_actual = slow_rate_limit(right_actual, right_target, step=5)

        left.spin(DirectionType.FORWARD, left_actual, VelocityUnits.PERCENT)
        right.spin(DirectionType.FORWARD, right_actual, VelocityUnits.PERCENT)
    '''

    lastpressed= False
    togle = False

    while True:
        forward = controller.axis3.position()
        turn = controller.axis1.position()

        if -5 < forward < 5:
            forward = 0

        if -5 < turn < 5:
            turn = 0
        
        left_speed = forward + turn
        right_speed = forward - turn

        left.spin(DirectionType.FORWARD, left_speed, VelocityUnits.PERCENT)
        right.spin(DirectionType.FORWARD, right_speed, VelocityUnits.PERCENT)

        if controller.buttonR1.pressing():
            intake.spin(FORWARD, 100, PERCENT)
        elif controller.buttonL1.pressing():
            intake.spin(REVERSE, 100, PERCENT)
        else:
            intake.stop()

        # pneumatic
        if lastpressed == False and controller.buttonR1.pressing():
            togle = not togle
            if togle: 
                match_load.open()
            else:
                match_load.close()         
        lastpressed = controller.buttonR1.pressing()

        wait(50)




#auton for later
def auton_rightLong():
    intake.spin(FORWARD, 100, PERCENT)
    drivetrain.drive_for(FORWARD, 500, MM)
    wait(50, MSEC) 
    intake.stop()
    drivetrain.turn_for(LEFT, 100, DEGREES)            
    drivetrain.drive_for(REVERSE, 240, MM)
    intake.spin(FORWARD, 100, PERCENT)
    wait(200, MSEC)
    intake.stop()
    wait(50, MSEC)
    drivetrain.turn_for(RIGHT, 35 , DEGREES)


 
Competition(driver_control, auton_rightLong)


        
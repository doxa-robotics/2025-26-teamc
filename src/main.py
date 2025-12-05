# ----------------------------------------------------------------------------- #
#                                                                               #        
#    Project:        Right Arcade Control                                       #
#    Module:         main.py                                                    #
#    Author:         VEX                                                        #
#    Created:        Fri Aug 05 2022                                            #
#    Description:    This example will use the right X/Y Controller             #
#                    axis to control the Clawbot.                               #
#                                                                               #                                                                          
#    Configuration:  V5 Clawbot (Individual Motors)                             #
#                    Controller                                                 #
#                    Claw Motor in Port 3                                       #
#                    Arm Motor in Port 8                                        #
#                    Left Motor in Port 1                                       #
#                    Right Motor in Port 10                                     #
#                                                                               #                                                                          
# ----------------------------------------------------------------------------- #

from vex import *
#import math

#  intitializing the important stuff
brain = Brain()
controller = Controller()

pneumatics = Pneumatics


#  motors
right1 = Motor(Ports.PORT3, False)
right2 = Motor(Ports.PORT2, False)
right3 = Motor(Ports.PORT1, False)

left1 = Motor(Ports.PORT9, True)
left2 = Motor(Ports.PORT7, True)
left3 = Motor(Ports.PORT6, True)

pneumatics1 = Pneumatics(brain.three_wire_port.a)

intake= Motor(Ports.PORT17, True)

#  motorgroups
left=MotorGroup(left1, left2, left3)
right=MotorGroup(right1, right2, right3)

inertial = Inertial(Ports.PORT15)

#def scale_input(x):
    #return (x * abs(x)) / 100 

'''

def slow_rate_limit(current_speed, target_speed, step=5):
    if target_speed > current_speed + step:
        return current_speed + step
    elif target_speed < current_speed - step:
        return current_speed - step
    else:
        return target_speed

'''
################################################################################
#  used to create a way for the robot to be able to functionably move on its own
drivetrain = SmartDrive(left,right, inertial)


def move(direction: DirectionType.DirectionType, distance: int, velocity=75):
    drivetrain.drive_for(direction, distance, MM, velocity, RPM)
################################################################################# 

#  the most important function
def driver_control(): 
    lastpressed= False
    spining= False
    
    '''
    left_actual = 0
    right_actual = 0
    '''

    while True:
        '''
        for = controller.axis3.position()
        tur = controller.axis1.position()

        # Deadzone filtering
        if -5 < for < 5:
            for = 0
        if -5 < tur < 5:
            tur = 0

        # Apply parabolic scaling
        forward = scale_input(for)
        turn = scale_input(tur)

        left_target = forward + turn
        right_target = forward - turn

        # Apply slow limiter for smooth decel
        left_actual = slow_rate_limit(left_actual, left_target, step=5)
        right_actual = slow_rate_limit(right_actual, right_target, step=5)

        left.spin(DirectionType.FORWARD, left_actual, VelocityUnits.PERCENT)
        right.spin(DirectionType.FORWARD, right_actual, VelocityUnits.PERCENT)


        '''
        forward = controller.axis3.position()
        turn = controller.axis1.position()

        if -5 < forward < 5:
            forward = 0

        if -5 < turn < 5:
            turn = 0
        
        left_speed = forward + turn
        right_speed = forward - turn

        if controller.buttonR1.pressing():
            intake.spin(DirectionType.FORWARD, 100, RPM)
        else:
            intake.stop()


        left.spin(DirectionType.FORWARD, left_speed, VelocityUnits.PERCENT)
        right.spin(DirectionType.FORWARD, right_speed, VelocityUnits.PERCENT)

        # intake
       
        if lastpressed == False and controller.buttonR1.pressing():
            spining = not spining
            if spining: 
                pneumatics1.open()
            else:
                pneumatics1.close
          
        lastpressed= controller.buttonR1.pressing()





        wait(50)

def auton_rightLong():
    '''score balls on the long goal'''
    drivetrain.drive_for(FORWARD, 300, MM)
    drivetrain.turn_for(LEFT, 45, DEGREES)   


    
Competition(driver_control, auton_rightLong)


        
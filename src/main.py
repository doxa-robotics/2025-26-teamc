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

#  motors
right1 = Motor(Ports.PORT3, False)
right2 = Motor(Ports.PORT2, False)
right3 = Motor(Ports.PORT1, False)
right4 = Motor(Ports.PORT13, True)

left1 = Motor(Ports.PORT9, True)
left2 = Motor(Ports.PORT7, True)
left3 = Motor(Ports.PORT6, True)
left4 = Motor(Ports.PORT18, False)


#  motorgroups
left=MotorGroup(left1, left2, left3, left4)
right=MotorGroup(right1, right2, right3, right4)

inertial = Inertial(Ports.PORT15)

#def scale_input(x):
    #return (x * abs(x)) / 100 

################################################################################
#  used to create a way for the robot to be able to functionably move on its own
all = DriveTrain(left,right)
all.set_timeout(4000)

def move(direction: DirectionType.DirectionType, distance: int, velocity=75):
    all.drive_for(direction, distance, MM, velocity, RPM)
################################################################################# 

#  the most important function
def driver_control(): 
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

        # Calculate motor speeds
        left_speed = forward + turn
        right_speed = forward - turn

        # Spin motors with scaled speed
        left.spin(DirectionType.FORWARD, left_speed, VelocityUnits.PERCENT)
        right.spin(DirectionType.FORWARD, right_speed, VelocityUnits.PERCENT)

        '''
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

        wait(20)

def Auton():
    move(FORWARD, 300)


    
Competition(driver_control, Auton)


        
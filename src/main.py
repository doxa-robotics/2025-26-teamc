#  import everything from the vex module
from vex import *

#  intitializing the important stuff
brain = Brain()
controller = Controller()

# upper additional parts
intake = Motor(Ports.PORT14)

#  motors
right1 = Motor(Ports.PORT20, True)
right2 = Motor(Ports.PORT11, True)
left1 = Motor(Ports.PORT10, False)
left2 = Motor(Ports.PORT18, False)

#  motorgroups
left=MotorGroup(left1, left2)
right=MotorGroup(right1, right2)

#  inertial(maybe wont use it)
inertial = Inertial(Ports.PORT15)

################################################################################
#  used to create a way for the robot to be able to functionably move on its own
all = DriveTrain(left,right)
all.set_timeout(4000)

def move(direction: DirectionType.DirectionType, distance: int, velocity=75):
    all.drive_for(direction, distance, MM, velocity, RPM)
#################################################################################

#  the most important function
def driver_control():

    lastpressed2= False
    lastpressed=False
    
    while True:

        lastpressed= False
        lastpressed2= False

        forward = controller.axis3.position()
        turn = controller.axis1.position()

        left_speed = forward + turn
        right_speed = forward - turn

        left.spin(DirectionType.FORWARD, left_speed, VelocityUnits.PERCENT)
        right.spin(DirectionType.FORWARD, right_speed, VelocityUnits.PERCENT)

        # intake
       
        

          # Right side for lever and roller
        if lastpressed2 == False and controller.buttonR1.pressing():
            if not intake.is_spinning():
                intake.spin(DirectionType.FORWARD, 50, PERCENT)
            else:
                intake.stop()
        lastpressed2= controller.buttonR1.pressing()


        wait(10)



def AUTON():
    move(FORWARD,960)

Competition(driver_control, AUTON)

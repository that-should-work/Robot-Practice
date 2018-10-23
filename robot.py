import wpilib
from wpilib.drive import DifferentialDrive

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):            #This function is called upon program startup and should be used for mapping everything

        #motors
        self.motorL = wpilib.Spark(0)                               #channel 0
        self.motorR = wpilib.Spark(1)                               #channel 1
        self.drive = DifferentialDrive(self.motorL, self.motorR)    #dive setup, differential is used with tank
        
        #solenoids
        self.arm = wpilib.DoubleSolenoid(0,0,1)                     #modul 0 channels 0 and 1
        self.claw = wpilib.DoubleSolenoid(0,2,3)                    #modul 0 channels 2 and 3

        #controller
        self.controller = wpilib.Joystick(1)
            #in code use the following for each button or joystick with Logitech in "D" mode
            #left joystick horizontal   -   self.controller.getX()
            #left joystick vertical     -   self.controller.getY()
            #right joystick horizontal  -   self.controller.getZ()
            #right joystick vertical    -   self.controller.getT()
            #button X                   -   self.controller.getButton(1)
            #button A                   -   self.controller.getButton(2)
            #button B                   -   self.controller.getButton(3)
            #button Y                   -   self.controller.getButton(4)
            #trigger top left           -   self.controller.getButton(5)
            #trigger top right          -   self.controller.getButton(6)
            #bumper bottom left         -   self.controller.getButton(7)      
            #bumper bottom right        -   self.controller.getButton(8)      
            #button Back                -   self.controller.getButton(9)
            #button Start               -   self.controller.getButton(10)
       
        self.timer = wpilib.Timer()

    def autonomousInit(self):       #This function is called once during autonomous

        self.timer.reset()
        self.timer.start()
    
    def autonomousPeriod(self):     #This function is called ~50/s during autonomous (don't use loops)

        if self.timer.get() < 3:
            self.drive.tankDrive(0.5, 0.5, squaredInputs = True)            #drive forward at half speed
        elif self.timer.get() < 5:
            self.drive.tankDrive(0.0, 0.0, squaredInputs = True)            #stop driving
        else:
            self.drive.tankDrive(-1, 1, squaredInputs = True)               #spin left until time runs out

    def teleopPeriod(self):         #This function is called ~50/s during teleop (don't use loops)

        self.drive.tankDrive(self.controller.getY(), self.controller.getAxis(4)) #drive setup is all done

        in_out = 'Off'              #check for simple button push
        if self.controller.getButton(5):
            in_out = 'Forward'
        elif self.controller.getButton(6):
            in_out = 'Reverse'
        
        self.claw.set(in_out)       #adjust claw based on button push

        up_down = 'Off'             #check for simple button push
        if self.controller.getButton(7):
            up_down = 'Forward'
        elif self.controller.getButton(8):
            up_down = 'Reverse'
        
        self.arm.set(up_down)       #adjust arm based on button push
    
if __name__ == "__main__":          #run the program
    wpilib.run(MyRobot)
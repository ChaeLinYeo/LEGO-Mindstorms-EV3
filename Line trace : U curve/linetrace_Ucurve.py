import ev3dev.ev3 as ev3
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor
from time import sleep

#sensor
cs = ev3.ColorSensor()
#so = Sound()
#so.beep()
speed = 100
rm = ev3.LargeMotor('outC')
lm = ev3.LargeMotor('outB')
greenflag=0

while(True):
    try:
        cs = ev3.ColorSensor()
        if(cs.color == 1):    #if color is black
            rm.run_to_rel_pos(position_sp=1080, speed_sp=speed)
            lm.run_to_rel_pos(position_sp=1080, speed_sp=speed)
        elif(cs.color == 3 and greenflag==0):    #if color is green
            #sleep(3)
            print("it is green")
            greenflag = 1
            rm.stop()
            lm.stop()
            sleep(3)
            rm.run_to_rel_pos(position_sp=1080, speed_sp=speed)
            lm.run_to_rel_pos(position_sp=1080, speed_sp=speed)
        elif(cs.color == 5):    #if color is red
            rm.stop()
            lm.stop()
            so = Sound()
            so.beep()
            break
        elif(cs.color == 6):   #if color is white
            rm.run_to_rel_pos(position_sp=1080, speed_sp=speed)
            lm.run_to_rel_pos(position_sp=1080, speed_sp=speed+375)
    except:
        #print(e)
        rm.stop()
        lm.stop()
        break
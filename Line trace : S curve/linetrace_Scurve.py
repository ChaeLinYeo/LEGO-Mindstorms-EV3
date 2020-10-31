import ev3dev.ev3 as ev3
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor
from time import sleep

#color sensor
cs_l = ev3.ColorSensor(ev3.INPUT_2)
#black:1 / green:3 / red:5 / white:6

speed = 190
rm = ev3.LargeMotor('outC')
lm = ev3.LargeMotor('outB')
greenflag = 0
flag = False
so = Sound()
so.beep()

while(True):
    try:
        if(cs_l.color==1):    #turn right
            print("turn left / color : ", cs_l.color)
            flag=True
            rm.run_to_rel_pos(position_sp=1440, speed_sp=speed-200)
            lm.run_to_rel_pos(position_sp=1440, speed_sp=speed+210)
        elif(greenflag==0 and cs_l.color==3):    #color is green
            if (80<=cs_l.green<=150 and cs_l.red<=80):
                print("it is green")
                print("green / color : ", cs_l.red, cs_l.green, cs_l.blue)
                greenflag = 1
                rm.stop()
                lm.stop()
                sleep(3)
                if flag==True:
                    print("flag true, turn right->left")
                    rm.run_to_rel_pos(position_sp=1440, speed_sp=speed+210)
                    lm.run_to_rel_pos(position_sp=1440, speed_sp=speed-200)
                elif flag==False:
                    print("flag false, turn left->right")
                    while(cs_l.color != 1):
                        rm.run_to_rel_pos(position_sp=1440, speed_sp=speed-200)
                        lm.run_to_rel_pos(position_sp=1440, speed_sp=speed+210)
        elif(cs_l.color==5):    #color is red
            #print("red / color : ", cs_l.color)
            rm.stop()
            lm.stop()
            so.beep()
            break
        else:   #turn left
            #print("turn left / color : ", cs_l.color)
            rm.run_to_rel_pos(position_sp=1440, speed_sp=speed+210)
            lm.run_to_rel_pos(position_sp=1440, speed_sp=speed-200)
    except:
        #print(e)
        rm.stop()
        lm.stop()
        break
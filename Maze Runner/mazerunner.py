import ev3dev.ev3 as ev3
from ev3dev2.sound import Sound
from ev3dev2.sensor.lego import ColorSensor
from time import sleep
import queue

cs = ev3.ColorSensor(ev3.INPUT_1)
cs_m = ev3.LargeMotor('outC')
bike_m_l = ev3.LargeMotor('outD')
bike_m_r = ev3.LargeMotor('outB')

#map scan
map = [[-1]*10 for _ in range(10)]   #10*10 matrix
speed = 56 #initial speed_sp
#speedup = 190   #when sensor switch direction
#speedup2 = 117  #after ith row speed
sp = 55 #initial position_sp
num = 1 #for print
iter = 0    #for count column

#find path
N = 10   # x lenght
M = 10  # y lengh
#strt_x = 0  #green x
#strt_y = 1  #green y
#dst_x = 9   #red x
#dst_y = 5   #red y

dir = [[1, 0], [0, 1], [-1, 0], [0, -1]]

flag = False

#calculate the shortest distance value
def weight():
    # 1:can go    / 0:can not go
    q = queue.Queue()
    check = [[-1]*10 for _ in range(10)]
    check[strt_x][strt_y] = 1
    q.put((strt_x,strt_y))
    #start bfs
    while (q.qsize() != 0):
        x = q.queue[0][0]
        y = q.queue[0][1]
        q.get()
        for i in range(4):
            xx = x + dir[i][0]
            yy = y + dir[i][1]
            if(xx < 0 or xx >= N or yy < 0 or yy >= M):
                continue
            if(map[xx][yy] == 0 or check[xx][yy] != -1):
                continue
            check[xx][yy] = check[x][y]+1
            q.put((xx, yy))
    return check

#order list for destination
def MakeOrder(check):
    stack=[]
    order=[]
    check[strt_x][strt_y] = 1
    stack.append((strt_x, strt_y))
    do_nothing = False
    while(len(stack) != 0):
        x = stack[-1][0]
        y = stack[-1][1]
        p = stack.pop()
        if(do_nothing):
            boundary_answer = check[p[0]][p[1]]
            boundary = order.pop()
            while(check[boundary[0]][boundary[1]] > boundary_answer):
                boundary = order.pop()
        order.append(p)
        do_nothing = True

        #start dfs
        for i in range(4):
            xx = x + dir[i][0]
            yy = y + dir[i][1]
            if (xx < 0 or xx >= N or yy < 0 or yy >= M):
                continue
            if (check[xx][yy] == -1):
                continue
            if(check[xx][yy] == check[x][y] + 1):
                if(check[xx][yy] == check[dst_x][dst_y] and xx != dst_x and yy != dst_y):
                    continue
                if((xx,yy) == (dst_x, dst_y)):
                    order.append((xx,yy))
                    return order
                stack.append((xx,yy))
                do_nothing = False
    return order


try:
    #map scan
    for i in range (10):
        while(iter<9):
            if(cs.color == 1):
                print(num,":",cs.color,"black")
                if i%2 == 0 :
                    map[i][iter] = 0
                elif i%2 == 1 :
                    map[i][-iter+9] = 0
                if iter == 0:
                    speed = speed+7
                if i >= 5:
                    if iter == 0:
                        speed = speed+8
                    else:
                        speed = speed+1
                if flag == False:
                    cs_m.run_to_rel_pos(position_sp=sp, speed_sp=speed)
                    sleep(3)
                elif flag == True:
                    cs_m.run_to_rel_pos(position_sp=-sp, speed_sp=speed)
                    sleep(3)
                cs_m.stop()
                iter += 1
                speed = 60
            elif(cs.color == 3 and 80 <= cs.green <= 150 and cs.red<=80):
                print(num,":",cs.color,"green")
                if i%2 == 0 :
                    map[i][iter] = 3
                elif i%2 == 1 :
                    map[i][-iter+9] = 3
                if iter == 0:
                    speed = speed+7
                if i >= 5:
                    if iter == 0:
                        speed = speed+8
                    else:
                        speed = speed+1
                if flag == False:
                    cs_m.run_to_rel_pos(position_sp=sp, speed_sp=speed)
                    sleep(3)
                elif flag == True:
                    cs_m.run_to_rel_pos(position_sp=-sp, speed_sp=speed)
                    sleep(3)
                cs_m.stop()
                iter += 1
                speed = 60
            elif(cs.color == 5):
                print(num,":",cs.color,"red")
                if i%2 == 0 :
                    map[i][iter] = 5
                elif i%2 == 1 :
                    map[i][-iter+9] = 5
                if iter == 0:
                    speed = speed+7
                if i >= 5:
                    if iter == 0:
                        speed = speed+8
                    else:
                        speed = speed+1
                if flag == False:
                    cs_m.run_to_rel_pos(position_sp=sp, speed_sp=speed)
                    sleep(3)
                elif flag == True:
                    cs_m.run_to_rel_pos(position_sp=-sp, speed_sp=speed)
                    sleep(3)
                cs_m.stop()
                iter += 1
                speed = 60
            else:
                print(num,":",cs.color,"white")
                if i%2 == 0 :
                    map[i][iter] = 1
                elif i%2 == 1:
                    map[i][-iter+9] = 1
                if iter == 0:
                    speed = speed+7
                if i >= 5:
                    if iter == 0:
                        speed = speed+8
                    else:
                        speed = speed+1
                if flag == False:
                    cs_m.run_to_rel_pos(position_sp=sp, speed_sp=speed)
                    sleep(3)
                elif flag == True:
                    cs_m.run_to_rel_pos(position_sp=-sp, speed_sp=speed)
                    sleep(3)
                cs_m.stop()
                iter += 1
                speed = 60
        print(num,":",cs.color)
        if cs.color == 1:#black
            if i%2==0:
                map[i][9] = 0
            elif i%2==1:
                map[i][0] = 0
        elif (cs.color == 3 and 80 <= cs.green <= 150 and cs.red <= 80):#green
            if i%2==0:
                map[i][9] = 3
            elif i%2==1:
                map[i][0] = 3
        elif cs.color == 5:#red
            if i%2==0:
                map[i][9] = 5
            elif i%2==1:
                map[i][0] = 5
        else:#white
            if i%2==0:
                map[i][9] = 1
            elif i%2==1:
                map[i][0] = 1
        num+=1
        iter=0
        if i == 9:
            break
        bike_m_l.run_to_rel_pos(position_sp=37, speed_sp=30)
        bike_m_r.run_to_rel_pos(position_sp=37, speed_sp=30)
        sleep(3)
        bike_m_l.stop()
        bike_m_r.stop()
        flag = not flag
        print("==============================")
    #if i>= 4:
    #    bike_m_l.run_to_rel_pos(position_sp=3600, speed_sp=200)
    #    bike_m_r.run_to_rel_pos(position_sp=3600, speed_sp=200)
    
    bike_m_l.run_to_rel_pos(position_sp=-3600, speed_sp=110)
    bike_m_r.run_to_rel_pos(position_sp=-3600, speed_sp=110)
    sleep(3)
    bike_m_l.stop()
    bike_m_r.stop()

    print("scanned map")
    for i in range(N):
        for j in range(M):
            print('{0:^2d}'.format(map[i][j]), end=",")
        print()

    for i in range(10):
        for j in range(10):
            if map[i][j] == 3:#green
                strt_x = i
                strt_y = j
            if map[i][j] == 5:#red
                dst_x = i
                dst_y = j

    #find shortest path
    check = weight()
    OrderList = MakeOrder(check)
    print("shortest path map")
    for i in range(N):
        for j in range(M):
            print('{0:^2d}'.format(check[i][j]), end=",")
        print()

    print("order list")
    print(OrderList)


    #follow the shortest path
    so = Sound()
    x = 0
    y = 0
    sleep(3)
    while(x != OrderList[0][0] or y != OrderList[0][1]):
        if OrderList[0][0] > x :
            bike_m_l.run_to_rel_pos(position_sp=37, speed_sp=30)
            bike_m_r.run_to_rel_pos(position_sp=37, speed_sp=31)
            sleep(2)
            x+=1
            continue
        if OrderList[0][0] < x:
            bike_m_l.run_to_rel_pos(position_sp=-37, speed_sp=30)
            bike_m_r.run_to_rel_pos(position_sp=-37, speed_sp=31)
            sleep(2)
            x-=1
            continue
        if OrderList[0][1] > y:
            cs_m.run_to_rel_pos(position_sp=sp, speed_sp=speed)
            sleep(2)
            y+=1
            continue
        if OrderList[0][1] < y:
            cs_m.run_to_rel_pos(position_sp=-sp, speed_sp=speed)
            sleep(2)
            y-=1
            continue
    sleep(3)
    so.beep()
    #for i in range(len(OrderList)+1):
    i=0
    while (dst_x != x or dst_y != y) :
        print(i, "th step", x, y)
        if (dst_x == x and dst_y == y):
            break
        if OrderList[i][0] > x :
            if i==0:
                bike_m_l.run_to_rel_pos(position_sp=37, speed_sp=30)
                bike_m_r.run_to_rel_pos(position_sp=37, speed_sp=31)
            else:
                bike_m_l.run_to_rel_pos(position_sp=37, speed_sp=30)
                bike_m_r.run_to_rel_pos(position_sp=37, speed_sp=31)
            sleep(2)
            x+=1
        if OrderList[i][0] < x :
            if i==0:
                bike_m_l.run_to_rel_pos(position_sp=-37, speed_sp=30)
                bike_m_r.run_to_rel_pos(position_sp=-37, speed_sp=31)
            else:
                bike_m_l.run_to_rel_pos(position_sp=-37, speed_sp=30)
                bike_m_r.run_to_rel_pos(position_sp=-37, speed_sp=31)
            sleep(2)
            x-=1
        if OrderList[i][1] > y :
            if i==0:
                cs_m.run_to_rel_pos(position_sp=sp, speed_sp=speed)
            else:
                cs_m.run_to_rel_pos(position_sp=sp, speed_sp=speed)
            sleep(2)
            y+=1
        if OrderList[i][1] < y :
            if i==0:
                cs_m.run_to_rel_pos(position_sp=-sp, speed_sp=speed)
            else:
                cs_m.run_to_rel_pos(position_sp=-sp, speed_sp=speed)
            sleep(2)
            y-=1
        i+=1
except:
    cs_m.stop()
    bike_m_l.stop()
    bike_m_r.stop()
so = Sound()
so.beep()
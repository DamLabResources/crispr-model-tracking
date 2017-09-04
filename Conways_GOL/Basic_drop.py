import time
from Tkinter import *

master = Tk()
WW = Canvas(master, width=500, height=500)
WW.pack()
#TEST_rect#   w.create_rectangle(0,0,55,55,fill='red')

w, h = 10, 10
Ma = [[0 for x in range(w)] for y in range(h)]
Ma[5][5] = 1

listN = [-1, 0, 1]

for x in Ma:
    print(x)
print

for x in range(10):
    new = []
    newO = []
    for a, x in enumerate(Ma):
        for b, y in enumerate(x):
            for Na in listN:
                for Nb in listN:
                    try:
                        ##### RULES #####
                        #if next to 1, become 1
                        if Ma [a+Na] [b+Nb] == 1:
                            new.extend([[a,b]])
                        #if 1, become 0
                        if y == 1:
                            newO.extend([[a,b]])

                    except:
                        pass

    #updates matrix w/list of new 1's
    for x in new:
        Ma [x[0]] [x[1]] =1

    # updates matrix w/list of new 0's
    for x in newO:
        Ma [x[0]] [x[1]] =0

    # std output matrix
    for x in Ma:
        print(x)
    print

    #draw matrix
    for a, x in enumerate(Ma):
        for b, y in enumerate(x):
            if y ==1:
                WW.create_rectangle(b*50, a*50, (b+1)*50, (a+1)*50, fill='red')
            else:
                WW.create_rectangle(b*50, a*50, (b+1)*50, (a+1)*50,fill='blue')

    #update drawing
    time.sleep(1)
    master.update()
mainloop()

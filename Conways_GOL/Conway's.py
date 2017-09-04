import time
from Tkinter import *

master = Tk()
WW = Canvas(master, width=500, height=500)
WW.pack()
#TEST_rect#   w.create_rectangle(0,0,55,55,fill='red')

#matrix dimensions
w, h = 10, 10
Ma = [[0 for x in range(w)] for y in range(h)]

######starting live cells
#blinker or square
#Ma[4][6] = 1;Ma[4][5] = 1;Ma[4][4] = 1 #;Ma[5][4] = 1
#glider
Ma[2][2] = 1;Ma[3][3] = 1;Ma[3][4] = 1;Ma[4][3] = 1;Ma[4][2] = 1

#distance from self to check for neighbors (currently 1)
listN = [-1, 0, 1]

#print starting matrix
for x in Ma:
    print(x)
print

###Main iteration
for x in range(20):
    print(x)
    new1 = []
    new0 = []
    #assess currenty layout and add modification to lists
    for a, x in enumerate(Ma):
        for b, y in enumerate(x):
            Ncounter = 0                #reset neighbor counter
            if Ma[a][b] == 1:
                Ncounter = Ncounter - 1
            for Na in listN:
                for Nb in listN:
                    try:
                        ##### Count live neighbors
                        if Ma[a + Na][b + Nb] == 1:
                            Ncounter = Ncounter + 1
                    except:
                        pass

            ##### RULES
            #Reproduction: Empty space(y=0) with 3 neighbors
            if y == 0 and Ncounter == 3:
                new1.extend([[a, b]])  # add to 1 list
            #Stasis: if 2 or 3 neighbors then survive
#not            if y ==1 and Ncounter == 2 or 3:
#working               new1.extend([[a, b]])         #add to 1 list, should already be 1 though
            #Overpopulation: more than 3 neighbors
            if y == 1 and Ncounter > 3:
                new0.extend([[a, b]])        #add to 0 list
            #Underpopulation: less than 2 neighbors
            if y == 1 and Ncounter < 2:
                new0.extend([[a, b]])       # add to 0 list

    #updates matrix w/list of new 1's
    for x in new1:
        Ma [x[0]] [x[1]] =1

    # updates matrix w/list of new 0's
    for x in new0:
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
    #time.sleep(.25)
    master.update()
mainloop()


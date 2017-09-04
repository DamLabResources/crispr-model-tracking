import time
from Tkinter import *

master = Tk()
WW = Canvas(master, width=600, height=600)
WW.pack()
#TEST_rect#   w.create_rectangle(0,0,55,55,fill='red')

#matrix dimensions
matrixLength=50
w, h = matrixLength, matrixLength
Ma = [[0 for x in range(w)] for y in range(h)]
cellSize=(500/matrixLength)

######starting live cells
#square
#Ma[1][5] = 1;Ma[1][6] = 1;Ma[1][7] = 1# ;Ma[5][4] = 1
#glider
#Ma[2][2] = 1;Ma[3][3] = 1;Ma[3][4] = 1;Ma[4][3] = 1;Ma[4][2] = 1
#Unbounded growth # best with 50x50 matrix
Ma[20][20]=1;Ma[20][22]=1;Ma[20][24]=1;Ma[19][21]=1;Ma[19][22]=1;Ma[19][24]=1;Ma[18][23]=1;Ma[18][24]=1;Ma[17][20]=1;Ma[16][20]=1;Ma[16][21]=1;Ma[16][22]=1;Ma[16][24]=1;

#distance from self to check for neighbors (currently 1)
listN = [-1, 0, 1]

#print starting matrix
for x in Ma:
    print(x)
print

###Main iteration
for xx in range(150):
    print(xx)
    new1 = []   #list for new 1's
    new0 = []   #and 0's
    #assess currenty layout and add modification to lists
    for a, x in enumerate(Ma):
        for b, y in enumerate(x):
            Ncounter = 0                #reset neighbor counter
            if Ma[a][b] == 1:           #remove self(Na,Nb=0) from neighb0ring 1's count, if 1
                Ncounter = Ncounter - 1
            for Na in listN:
                NaA = a + Na
                if NaA == -1:
                    NaA = (matrixLength -2)
                if NaA == matrixLength:
                    NaA = 1
                for Nb in listN:
                    NbB = b + Nb
                    if NbB == -1:
                        NbB = (matrixLength-2)
                    if NbB == matrixLength:
                        NbB = 1

#                    try:
                        ##### Count live neighbors
                    if Ma[NaA][NbB] == 1:
                        Ncounter = Ncounter + 1
#                    except:
#                        pass

            ##### RULES
            #Reproduction: Empty space(y=0) with 3 neighbors
            if y == 0 and Ncounter == 3:
                new1.extend([[a, b]])  # add to 1 list
            #Stasis: if 2 or 3 neighbors then survive
            if y ==1 and Ncounter == 2 or Ncounter == 3 :
               new1.extend([[a, b]])         #add to 1 list, should already be 1 though
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
    WW.delete(ALL)              #delete previous drawing
    for a, x in enumerate(Ma):
        for b, y in enumerate(x):
            if y ==1:
                WW.create_rectangle(b*cellSize, a*cellSize, (b+1)*cellSize, (a+1)*cellSize, fill='red')
            else:
                WW.create_rectangle(b*cellSize, a*cellSize, (b+1)*cellSize, (a+1)*cellSize,fill='blue')

    #update drawing
#    time.sleep(.1)     #delay between refresh
    master.update()
mainloop()
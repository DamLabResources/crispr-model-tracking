import time
from Tkinter import *

master = Tk()
WW = Canvas(master, width=800, height=800)
WW.pack()

#matrix dimensions
matrixLength=15
w, h = matrixLength, matrixLength
Ma = [[0 for x in range(w)] for y in range(h)]
cellSize=(500/matrixLength)

#distance from self to check for neighbors (currently 1)
listN = [-1, 0, 1]

#initialize lists
new1 = []               #list of "cells"
new0 = []

### STARTERS
new1.extend([[5,5]])

for x in new1:
    print()





#updates matrix w/list of new 1's
for x in new1:
    Ma [x[0]] [x[1]] =1

#draw matrix
for a, x in enumerate(Ma):
    for b, y in enumerate(x):
        if y ==1:
            WW.create_rectangle(b*cellSize, a*cellSize, (b+1)*cellSize, (a+1)*cellSize, fill='red')
        else:
            WW.create_rectangle(b*cellSize, a*cellSize, (b+1)*cellSize, (a+1)*cellSize,fill='blue')

mainloop()
import numpy as np
from tkinter import *
import time

class Box(object):

    def __init__(self, typ):

        self.typ = typ
        self.new_typ = self.typ     #was None


    def decide(self, neighbors):

        ##### RULES (CONWAY'S GAME OF LIFE)
        # remove self count of 1 for counting "1" neighbors
        num_ones = sum(box.typ == 1 for box in neighbors.flatten())
        if self.typ == 1:
            num_ones -= 1
        # Reproduction: Empty space(y=0) with 3 neighbors
#        if self.typ == 0 and num_ones == 3:
#            self.new_typ = 1
        # Stasis: if 2 or 3 neighbors then survive
        elif self.typ == 1 and (num_ones == 2 or num_ones == 3):
            self.new_typ = 1       # add to 1 list, should already be 1 though
        # Overpopulation: more than 3 neighbors
#        elif self.typ == 1 and num_ones > 3:
#            self.new_typ = 0
        # Underpopulation: less than 2 neighbors
        elif self.typ == 1 and num_ones < 2:
            self.new_typ = 0      # add to 0 list
        else:
            #print(self.typ, num_ones)
            self.new_typ = self.typ


    def update(self):

        if self.new_typ is None:
            raise AssertionError('Type not decided')

        self.typ = self.new_typ
        self.new_typ = None

    def color(self):

        if self.typ == 0:
            return 'blue'
        elif self.typ == 1:
            return 'red'
        else:
            raise KeyError

    def colrNbr(self):
        return 'yellow'



class Population(object):

    def __init__(self, xdim, ydim, canvas):

        self.xdim = xdim
        self.ydim = ydim
        self.canvas = canvas

        self.cellSize=(500/self.xdim)

    def initialize(self, frac_ones):

        items = self.xdim*self.ydim
        #random
        #ar = np.array([Box(np.random.rand()<frac_ones) for _ in range(items)])
        #Defined:
        ar = np.array([Box(0) for _ in range(items)])
        #glider
        #ar[1] = Box(1);ar[12] = Box(1);ar[13] = Box(1);ar[22] = Box(1);ar[21] = Box(1)
        #ar[0] = Box(1);ar[99] = Box(1);ar[9] = Box(1);ar[90] = Box(1);
        ar[99] = Box(1);

        self.population = ar.reshape(self.xdim, self.ydim)


    def cycle(self):

        for x in range(self.xdim):
            for y in range(self.ydim):
                box = self.population[x, y]
                if x > 0 and y > 0:
                    box2 = self.population[x-1, y-1]
                if box.typ ==1:
                    box2.new_typ = 1
                neighbors = self.get_neighbors(x, y)
                box.decide(neighbors)

        for box in self.population.flatten():
            box.update()

    def get_neighbors(self, x, y):
        ### RETURNS MATRIX OF 9 BOX NEIGHBORS AND 0,0 SELF
        edgex =0
        edgey =0
        if x == 0:
            edgex =1
        if y == 0:
            edgey =1
        neighbors = self.population[(x-1+edgex):(x+2), (y-1+edgey):(y+2)]
        return neighbors

    def stdOut(self):
        for x in range(self.xdim):
            counts = []
            for y in range(self.ydim):
                box = self.population[x, y]
                counts.append(box.typ)
            print(counts)

    def draw(self):

        self.canvas.delete(ALL)              #delete previous drawing
        for a in range(self.xdim):
            for b in range(self.ydim):
                box = self.population[a, b]
                self.canvas.create_rectangle(b*self.cellSize,
                                                 a*self.cellSize,
                                                 (b+1)*self.cellSize,
                                                 (a+1)*self.cellSize, fill=box.color())





if __name__ == '__main__':

    master = Tk()
    WW = Canvas(master, width=600, height=600)
    WW.pack()
    pop = Population(15, 15, WW)
    pop.initialize(0.1)

    pop.stdOut()
    for mLoop in range(500):
        print(mLoop, ":", sum(box.typ == 1 for box in pop.population.flatten()))
        WW.delete(ALL)
        pop.cycle()
        pop.draw()
        master.update()
        pop.stdOut()
        #raise KeyboardInterrupt
        #time.sleep(.5)
mainloop()
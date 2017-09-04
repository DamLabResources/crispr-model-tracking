import numpy as np
from tkinter import *
import time

class Box(object):

    def __init__(self, typ):

        self.typ = typ
        self.new_typ = None

    def decide(self, neighbors):

        num_ones = sum(box.typ == 1 for box in neighbors.flatten())

        ##### RULES
        # Reproduction: Empty space(y=0) with 3 neighbors
        if self.typ and num_ones == 3:
            self.new_typ = True
        # Stasis: if 2 or 3 neighbors then survive
        elif self.typ and (num_ones == 2 or num_ones == 3):
            self.new_typ = True       # add to 1 list, should already be 1 though
        # Overpopulation: more than 3 neighbors
        elif self.typ and num_ones > 3:
            self.new_typ = False
        # Underpopulation: less than 2 neighbors
        elif self.typ and num_ones < 2:
            self.new_typ = False      # add to 0 list
        else:
            #print(self.typ, num_ones)
            self.new_typ = True

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



class Population(object):

    def __init__(self, xdim, ydim, canvas):

        self.xdim = xdim
        self.ydim = ydim
        self.canvas = canvas

        Ma = [[0 for x in range(self.xdim)] for y in range(self.ydim)]
        self.cellSize=(500/self.xdim)

    def initialize(self, frac_ones):

        items = self.xdim*self.ydim

        ar = np.array([Box(np.random.rand()<frac_ones) for _ in range(items)])
        self.population = ar.reshape(self.xdim, self.ydim)

    def cycle(self):

        for x in range(self.xdim):
            for y in range(self.ydim):
                box = self.population[x, y]
                neighbors = self.get_neighbors(x, y)
                box.decide(neighbors)

        for box in self.population.flatten():
            box.update()

    def get_neighbors(self, x, y):
        neighbors = self.population[x-1:x+1, y-1:y+1]
        return neighbors

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


    pop = Population(20, 20, WW)
    pop.initialize(0.5)
    for _ in range(30):
        pop.cycle()
        pop.draw()
        master.update()
        print(sum(box.typ == 1 for box in pop.population.flatten()))
        #raise KeyboardInterrupt
        time.sleep(5)

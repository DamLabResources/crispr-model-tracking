import numpy as np
from tkinter import *
import time

class register(object):
    def __init__(self, lineage, gRNA):

        self.lineage = lineage
        self.gRNA = list(gRNA)
        self.progeny = 1
        self.persister = False

    def extend(self):
        newL = str(self.lineage) + "." + str(self.progeny)
        self.progeny +=1
        return newL

    def mutate(self):
        nList=["A", "T", "C", "G"]
        newG = list(self.gRNA)
        mutLength = np.random.random_integers(5)
        startmut = np.random.random_integers(0,19)
        if startmut + mutLength > 19:
            endmut = 19
        else:
            endmut = startmut + mutLength

        while startmut < endmut:
            newG[startmut] = np.random.choice(nList)
            startmut+=1
        return newG

    def getlineage(self):           #unused?
        return self.lineage

    def sequence(self):             #unused?
        return self.gRNA

class Box(object):

    def __init__(self, typ):

        self.typ = typ
        self.new_typ = self.typ     #was None


    def decide(self, neighbors):
        #####   FOR MODIFYING NEIGHBORS
        ones=[]
        zeros=[]
        zeroNT=[]
        if type(self.typ) == register:
            for x in neighbors.flatten():
                if type(x.typ) == register:
                    ones.append(x)
                elif x.typ == 0:
                    zeros.append(x)
            #print(len(ones), len(zeros))

            if self.typ.persister == True:
                divisionRate = 0.05
            else:
                divisionRate = 0.33333333333

            if len(zeros)>0:
                if np.random.rand()<divisionRate:
                    for l in zeros:
                        if type(l.new_typ) != register:
                            zeroNT.append(l)
                    if len(zeroNT) > 0:
                        daughterCell= np.random.choice(zeroNT)
                        daughterCell.new_typ = register(self.typ.extend(),self.typ.mutate())
                        if np.random.rand()<0.05:
                            daughterCell.new_typ.persister = True

            self.new_typ = self.typ
        else:
            if self.new_typ is None:
                self.new_typ = 0

    def update(self):

        if self.new_typ is None:
            raise AssertionError('Type not decided')

        self.typ = self.new_typ
        self.new_typ = None

    def color(self):

        if self.typ == 0:
            return 'blue'
        elif type(self.typ) == register:
            return 'red'
        else:
            raise KeyError


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
        ar[99] = Box(register(1,"AAAAAAAAAAAAAAAAAAAA"));

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
        ### RETURNS MATRIX OF 9 BOX NEIGHBORS AND 0,0 SELF
        edgex =0
        edgey =0
        if x == 0:
            edgex =1
        if y == 0:
            edgey =1
        neighbors = self.population[(x-1+edgex):(x+2), (y-1+edgey):(y+2)]
        return neighbors

    def antibiotics(self):
        dead = 0
        survived = 0
        for x in range(self.xdim):
            for y in range(self.ydim):
                box = self.population[x, y]
                if isinstance(box.typ,register):
                    if box.typ.persister == False:
                        box.typ = 0
                        dead += 1

                    else:
                        survived +=1
        print("Killed by Antibiotics: ", dead, "\n", "Survived: ", survived)

    def stdOut(self):
        for x in range(self.xdim):
            counts = []
            for y in range(self.ydim):
                box = self.population[x, y]
                if box.typ == 0:
                    counts.append(box.typ)
                elif type(box.typ) == register:
                    counts.append(1)
            print(counts)

    def printlineages(self):
        for box in self.population.flatten():
            if type(box.typ) == register:
                print("".join(box.typ.gRNA), "\t", box.typ.lineage, "\t", box.typ.persister)

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
        print()
        WW.delete(ALL)
        pop.cycle()
        print(mLoop, ":", sum(type(box.typ) == register for box in pop.population.flatten()))
        if mLoop%25 == 0 and mLoop > 24:
            pop.antibiotics()
        pop.stdOut()
        pop.printlineages()
        pop.draw()
        master.update()
        #raise KeyboardInterrupt
        time.sleep(.5)
mainloop()
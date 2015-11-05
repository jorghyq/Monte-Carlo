# main class solver will be defined here
import sys


class Solver():
    def __init__(self, elements):
        # default settings of the lattice
        self.length = 20
        self.width = 20
        self.MAX_RUN = 100000
        self.elements = elements

    def init(self):
        # TODO: initialize the elements

    def step(self, step_num):
        if step_num <= 0:
            print "step number should be positve integer"
        else:
            while step_num > 0:
                pass


import math

#1-D lattice total energy function evaluator class
#
class Particles1D:
    selfEnergy=None
    interactionEnergy=None

    @classmethod
    def fitnessFunc(cls,state):
        totalEnergy=0
        for i in range(len(state)):
            #self energy
            totalEnergy+=cls.selfEnergy[state[i]]
            #interaction energy
            if i == 0: totalEnergy+=cls.interactionEnergy[state[i]][state[i+1]]
            elif i == len(state)-1: totalEnergy+=cls.interactionEnergy[state[i-1]][state[i]]
            else: totalEnergy+=cls.interactionEnergy[state[i-1]][state[i]] + cls.interactionEnergy[state[i]][state[i+1]]

        return -totalEnergy


#Multi-dimensional Rastrigrin function evaluator class
#
class Rastrigrin:
    nVars=None
    A=None

    @classmethod
    def fitnessFunc(cls,state):
        fitness=cls.A*cls.nVars

        for i in range(cls.nVars):
            fitness+=state[i]*state[i] - cls.A*math.cos(2.0*math.pi*state[i])

        return -fitness


#Mean squared error class
#
class MSE:
    nVars=None
    mDegrees=None
    dataX=None
    dataY=None


    @classmethod
    def poly_sum(cls, x, state):
        rst = 0
        for i in range(cls.mDegrees+1):
            rst+=state[i]*(x**i)
        return rst

    @classmethod
    def fitnessFunc(cls,state):
        fitness=0

        for i in range(cls.nVars):
            fitness+=(cls.dataY[i]-cls.poly_sum(cls.dataX[i], state))**2
        #    fitness+=state[i]*state[i] - cls.A*math.cos(2.0*math.pi*state[i])

        return -fitness/cls.nVars


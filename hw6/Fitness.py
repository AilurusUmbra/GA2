import math


# 1-D lattice total energy function evaluator class
class Lattice:
    selfEnergy = None
    interactionEnergy = None

    @classmethod
    def fitnessFunc(cls, x):
        totalEnergy = 0
        for i in range(len(x)):
            # self energy
            totalEnergy += cls.selfEnergy[x[i]]
            # interaction energy
            if i == 0:
                totalEnergy += cls.interactionEnergy[x[i]][x[i+1]]
            elif i == len(x)-1:
                totalEnergy += cls.interactionEnergy[x[i-1]][x[i]]
            else:
                totalEnergy += cls.interactionEnergy[x[i-1]][x[i]] + cls.interactionEnergy[x[i]][x[i+1]]

        return -totalEnergy


# Multi-dimensional Rastrigrin function evaluator class
class Rastrigrin:
    nVars = None
    A = None

    @classmethod
    def fitnessFunc(cls, x):
        fitness = cls.A*cls.nVars

        for i in range(cls.nVars):
            fitness += x[i]*x[i] - cls.A*math.cos(2.0*math.pi*x[i])

        return -fitness

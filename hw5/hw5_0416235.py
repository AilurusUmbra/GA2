#
#
#  To run: python hw5_0416235.py --input hw5_0416235.cfg
#
#

import optparse
import sys
import yaml
import math
from random import Random
import numpy as np
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 4, figsize=(16,4))
ax[0].set_title("best")
ax[1].set_title("avg & stdev")
ax[2].set_title("Fitness Function")
ax[3].set_title("adaptive sigma")
plt.ion()
plt.show()

pausetime=0.5


def plotFitnessFunc(fitnessFunc, minLimit, maxLimit, granularity=100):
    x1 = np.linspace(minLimit, maxLimit, num=granularity)
    y = []
    for x in x1:
        y.append(fitnessFunc(x))
    ax[2].plot(x1, y)


def plotGeneration(pop):
    mpl_pts = []
    for p in pop:
        mpl_pt = ax[2].scatter(p.x, p.fit)
        mpl_pts.append(mpl_pt)
    plt.pause(pausetime)
    return mpl_pts


def removePlotGeneration(mpl_pts):
    for pt in mpl_pts:
        pt.remove()

# EV2 Config class
class EV2_Config:
    """
    EV2 configuration class
    """
    #  class variables
    sectionName = 'EV2'
    options = {'populationSize': (int, True),
               'generationCount': (int, True),
               'randomSeed': (int, True),
               'minLimit': (float, True),
               'maxLimit': (float, True)}

    # constructor
    def __init__(self,  inFileName):
        infile = open(inFileName, 'r')
        ymlcfg = yaml.load(infile)
        infile.close()
        eccfg = ymlcfg.get(self.sectionName, None)
        if eccfg is None:
            raise Exception('Missing EV2 section in cfg file')

        # iterate over options
        for opt in self.options:
            if opt in eccfg:
                optval = eccfg[opt]

                # verify parameter type
                if type(optval) != self.options[opt][0]:
                    raise Exception('Parameter "{}" has wrong type'.format(opt))

                # create attributes on the fly
                setattr(self, opt, optval)
            else:
                if self.options[opt][1]:
                    raise Exception('Missing mandatory parameter "{}"'.format(opt))
                else:
                    setattr(self, opt, None)

    # string representation for class data
    def __str__(self):
        return str(yaml.dump(self.__dict__, default_flow_style=False))


# Simple 1-D fitness function example
#
def fitnessFunc(x):
    # This function will get stuck with Newton method if start at -1 or 1
    # max = 3.9622, when x^2 = 0.5*(1+sqrt(17))
    # return (-1/6)*x**6 + (1/4)*x**4 + 2*x**2
    return -10 - (0.04*x)**2 + 10*math.cos(0.04*math.pi*x)


# Find index of worst individual in population
def findWorstIndex(l):
    minval = l[0].fit
    imin = 0
    for i in range(len(l)):
        if l[i].fit < minval:
            minval = l[i].fit
            imin = i
    return imin


points = []


# Print some useful stats to screen
def printStats(pop, gen):
    global points
    removePlotGeneration(points)
    print('Generation:', gen)
    maxval = pop[0].fit
    sigma = pop[0].sigma

    fitlist = [x.fit for x in pop]
    for p in pop:
        if p.fit > maxval:
            maxval = p.fit
            sigma = p.sigma
        print(str(p.x)+'\t'+str(p.fit)+'\t'+str(p.sigma))

    print('Max fitness', maxval)
    print('Avg fitness', np.mean(fitlist))
    print('Mutation rate', sigma)
    print('')
    points = plotGeneration(pop)

    return maxval, np.mean(fitlist), np.std(fitlist), sigma


# A trivial Individual class
class Individual:
    minSigma = 0.0001
    maxSigma = 1
    learningRate = 1  # n = 1, take learningRate = 1/n^0.5 = 1
    minLimit = None
    maxLimit = None
    prng = None

    def __init__(self, randomInit=True):
        if randomInit:
            self.x = self.prng.uniform(self.minLimit, self.maxLimit)
            self.fit = fitnessFunc(self.x)
            self.sigma = self.prng.uniform(0.9, 0.1)
        else:
            self.x = 0
            self.fit = 0
            self.sigma = self.minSigma

    def crossover(self, parent2):
        child = Individual(randomInit=False)
        alpha = self.prng.random()
        child.x = self.x*alpha + parent2.x*(1-alpha)
        child.sigma = self.sigma*alpha + parent2.sigma*(1-alpha)

        return child

    def mutate(self):
        self.sigma = self.sigma*math.exp(self.learningRate*self.prng.normalvariate(0,1))
        if self.sigma < self.minSigma:
            self.sigma = self.minSigma
        if self.sigma > self.maxSigma:
            self.sigma = self.maxSigma
        # use max-min to tune the convegence
        self.x = self.x+(self.maxLimit-self.minLimit)*self.sigma*self.prng.normalvariate(0,1)

    def evaluateFitness(self):
        self.fit = fitnessFunc(self.x)


# EV2: hw5 for self-adapted sigma
#
def ev2(cfg):
    #  start random number generator
    prng = Random()
    prng.seed(cfg.randomSeed)

    # set Individual static params: min/maxLimit, fitnessFunc, & prng
    Individual.minLimit = cfg.minLimit
    Individual.maxLimit = cfg.maxLimit
    Individual.prng = prng

    # random initialization of population
    population = []
    for i in range(cfg.populationSize):
        ind=Individual()
        ind.evaluateFitness()
        population.append(ind)

    # print stats
    input("Press any key to start")
    printStats(population, 0)

    # evolution main loop
    for i in range(cfg.generationCount):

        children = []
        # generate 5 children
        for j in range(5):
            # randomly select two parents
            parents = prng.sample(population, 2)

            # recombine using stochastic interplolation
            childx = parents[0].crossover(parents[1])

            # random mutation using self-adapted sigma
            childx.mutate()
            # update child's fitness value
            childx.evaluateFitness()

            children.append(childx)

        # survivor selection: replace worst
        for j in range(5):
            #child = Individual(childx, fitnessFunc(childx))
            iworst = findWorstIndex(population)
            if children[j].fit > population[iworst].fit:
                population[iworst] = children[j]

        # print stats
        _best, _avg, _std, _sigma = printStats(population, i+1)

        # store plot metrics
        ax[0].scatter(i, _best, c='b')
        ax[0].legend(['best fitness'])
        ax[1].scatter(i, _avg, c='g')
        ax[1].scatter(i, _std, c='r')
        ax[1].legend(['avg', 'stdev'], title="Statistics")
        ax[3].scatter(i, _sigma, c='b')
        ax[3].legend(['sigma'])


#
#  Main entry point
#
def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        #
        #  get command-line options
        #
        parser = optparse.OptionParser()
        parser.add_option("-i", "--input", action="store", dest="inputFileName", help="input filename", default=None)
        parser.add_option("-q", "--quiet", action="store_true", dest="quietMode", help="quiet mode", default=False)
        parser.add_option("-d", "--debug", action="store_true", dest="debugMode", help="debug mode", default=False)
        (options, args) = parser.parse_args(argv)

        # validate options
        if options.inputFileName is None:
            raise Exception("Must specify input file name using -i or --input option.")

        # Get EV2 config params
        cfg = EV2_Config(options.inputFileName)

        # print config params
        print(cfg)

        # run EV2
        plotFitnessFunc(fitnessFunc, cfg.minLimit, cfg.maxLimit, 200)
        ev2(cfg)
        #result_plot.pause(10)

        if not options.quietMode:
            print('EV2 Completed!')

    except Exception as info:
        if 'options' in vars() and options.debugMode:
            from traceback import print_exc
            print_exc()
        else:
            print(info)


if __name__ == '__main__':
    main()
    input("Press any key to exit")

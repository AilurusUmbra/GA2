#
# Individual.py
#
#

import math

#Base class for all individual types
#
class Individual:
    """
    Individual
    """
    init_mutRate=0.1
    minMutRate=1e-100
    maxMutRate=1
    learningRate=None
    uniprng=None
    normprng=None
    fitFunc=None

    def __init__(self):
        self.fit=self.__class__.fitFunc(self.state)
        self.ind_length = len(self.state)
        #self.mutRate=self.uniprng.uniform(0.9,0.1) #use "normalized" sigma
        self.mutRate=self.ind_length*[self.init_mutRate]
        self.learningRate=(2*(self.ind_length)**0.5)**(-0.5)
        self.poplearningRate=(2*self.ind_length)**(-0.5)

    def mutateMutRate(self):
        #self.mutRate=self.mutRate*math.exp(self.learningRate*self.normprng.normalvariate(0,1))
        #if self.mutRate < self.minMutRate: self.mutRate=self.minMutRate
        #if self.mutRate > self.maxMutRate: self.mutRate=self.maxMutRate
        for i in range(self.ind_length):
            self.pop_step = self.poplearningRate * self.normprng.normalvariate(0,1)
            self.ind_step = self.learningRate * self.normprng.normalvariate(0,1)
            self.mutRate[i] = self.mutRate[i] * math.exp(self.pop_step+self.ind_step)
            if self.mutRate[i] < self.minMutRate:
                self.mutRate[i] = self.minMutRate
            if self.mutRate[i] > self.maxMutRate:
                self.mutRate[i] = self.maxMutRate



    def evaluateFitness(self):
        if self.fit == None: self.fit=self.__class__.fitFunc(self.state)


#A combinatorial integer representation class
#
class IntVectorIndividual(Individual):
    """
    IntVectorIndividual
    """
    nLength=None
    nItems=None

    def __init__(self):
        self.state=[]
        for i in range(self.nLength):
            self.state.append(self.uniprng.randint(0,self.nItems-1))

        super().__init__() #call base class ctor

    def crossover(self, other):
        #perform crossover "in-place"
        for i in range(self.nLength):
            if self.uniprng.random() < 0.5:
                tmp=self.state[i]
                self.state[i]=other.state[i]
                other.state[i]=tmp

        self.fit=None
        other.fit=None

    def mutate(self):
        self.mutateMutRate() #update mutation rate

        for i in range(self.nLength):
            if self.uniprng.random() < self.mutRate:
                self.state[i]=self.uniprng.randint(0,self.nItems-1)

        self.fit=None

    def __str__(self):
        return str(self.state)+'\t'+'%0.8e'%self.fit+'\t'+'%0.8e'%self.mutRate


#Multivariate real representation class
#
class MultivariateIndividual(Individual):
    """
    MultivariateIndividual
    """
    nLength=None
    minLimit=None
    maxLimit=None

    def __init__(self):
        self.state=[]
        for i in range(self.nLength):
            self.state.append(self.uniprng.uniform(self.minLimit,self.maxLimit))

        super().__init__() #call base class ctor

    def crossover(self, other):
        #perform crossover "in-place"
        alpha=self.uniprng.random()

        for i in range(self.nLength):
            tmp=self.state[i]*alpha+other.state[i]*(1-alpha)
            other.state[i]=self.state[i]*(1-alpha)+other.state[i]*alpha
            self.state[i]=tmp

            if self.state[i] > self.maxLimit: self.state[i]=self.maxLimit
            if self.state[i] < self.minLimit: self.state[i]=self.minLimit
            if other.state[i] > self.maxLimit: other.state[i]=self.maxLimit
            if other.state[i] < self.minLimit: other.state[i]=self.minLimit

        self.fit=None
        other.fit=None

    def mutate(self):
        self.mutateMutRate() #update mutation rate

        for i in range(self.nLength):
            self.state[i]=self.state[i]+(self.maxLimit-self.minLimit)*self.mutRate[i]*self.normprng.normalvariate(0,1)
            if self.state[i] > self.maxLimit: self.state[i]=self.maxLimit
            if self.state[i] < self.minLimit: self.state[i]=self.minLimit

        self.fit=None

    def evaluateFitness(self):
        if self.fit == None: self.fit=self.__class__.fitFunc(self.state)

    def __str__(self):
        return str(self.state)+'\t'+'%0.8e'%self.fit+'\t'+ str(self.mutRate)


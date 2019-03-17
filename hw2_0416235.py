import yaml


# Argument Parser
import argparse
parser = argparse.ArgumentParser(description='Validating YAML file...')
parser.add_argument('-i', '--inputFile', type=str, help='input filename', required=True)
parser.add_argument('-o', '--outputFile', type=str, help='output filename', required=True)
parser.add_argument('-q', '--quiet', action="store_true", help='quiet mode', default=False)
args = parser.parse_args()


# Read input yaml
inputyaml = yaml.load(open(args.inputFile, "r"))


# Class initialization
class Engine:

    mandatoryParams = ['populationSize', 'generationCount', 'evaluatorType']
    missingParams = []
    incorrectTypes = []
    exceptParams = []

    def checkEngine(self, name):
        try:
            assert name == 'EC_Engine', "Warning: Wrong engine name"
        except AssertionError:
            if not args.quiet:
                print("*** Warning: Wrong engine name:", name, "***")
                print("Create new engine instance...\n")
            self.missingParams.append('EC_Engine')

    def checkMissingParams(self, dictionary):
        for p in self.mandatoryParams:
            if p not in dictionary.keys():
                self.missingParams.append(p)

        try:
            assert len(self.missingParams) == 0, "Error: Missing parameters"
        except AssertionError:
            if not args.quiet:
                print("*** Error: Missing parameters:", self.missingParams, "***")
                print("Use default values instead...")
                for p in self.missingParams:
                    print(p, getattr(self, p))
                print()

    def checkTypes(self, dictionary):
        for p in dictionary.keys():
            if type(vars(self)[p]) != type(dictionary[p]):
                self.incorrectTypes.append(p)
                dictionary[p] = getattr(self, p)
        try:
            assert len(self.incorrectTypes) == 0, "Error: Incorrect types"
        except AssertionError:
            if not args.quiet:
                print("*** Error: Incorrect types:", self.incorrectTypes, "***")
                print("Use default values instead...")
                for p in self.incorrectTypes:
                    print(p, getattr(self, p))
                print()


    def setDefault(self):
        self.populationSize = 100
        self.generationCount = 50
        self.evaluatorType = 'parabola'

        self.jobName = 'test'
        self.randomSeed = 10
        self.scalingParam = 2.5

    def checkExcept(self, dictionary):
        for p in dictionary.keys():
            if p not in vars(self).keys():
                self.exceptParams.append(p)
        try:
            assert len(self.exceptParams) == 0, "Warning: Exception parameters"
        except AssertionError:
            if not args.quiet:
                print("*** Warning: Exception parameter occurs... ***")
                print('exception parameter: ', self.exceptParams)
                print()
            for p in self.exceptParams:
                dictionary.pop(p)

    def __init__(self, dictionary, name='EC_Engine'):

        # set default schema
        self.setDefault()

        # check exception parameters
        self.checkExcept(dictionary)

        # check incorrect types
        self.checkTypes(dictionary)

        # check missing parameters
        self.checkMissingParams(dictionary)

        # assign engine name
        self.checkEngine(name)
        self.name = name

        # assign other parameters
        for k, v in dictionary.items():
            setattr(self, k, v)


for k in inputyaml.keys():
    e1 = Engine(inputyaml[k], k)

# print("e1: ", vars(e1))


# Write validation results
validation = {'missingParams': sorted(e1.missingParams),
              'incorrectTypes': sorted(e1.incorrectTypes)}
with open(args.outputFile, 'w') as outfile:
    yaml.dump(validation, outfile, default_style=False)


# quite mode
if not args.quiet:
    print(validation)

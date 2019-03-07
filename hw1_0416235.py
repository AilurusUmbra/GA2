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


# Variable initialization
schema = {'EC_Engine': {'populationSize': 100,
  'generationCount': 50,
  'randomSeed': 10,
  'evaluatorType': 'parabola',
  'jobName': 'test',
  'scalingParam': 2.5}}
mandatoryParams = ['populationSize', 'generationCount', 'evaluatorType']
missingParams = []
incorrectTypes = []
exceptParams = []


# Validation
if 'EC_Engine' in inputyaml.keys():
    # check missing parameters
    for p in mandatoryParams:
        if p not in inputyaml['EC_Engine'].keys():
            missingParams.append(p)

    # check incorrect types
    try:
        for p in inputyaml['EC_Engine'].keys():
            if type(schema['EC_Engine'][p]) != type(inputyaml['EC_Engine'][p]):
                incorrectTypes.append(p)
    except:
        exceptParams.append(p)
        print("Exception occurs...")
        print('exception parameter: ', exceptParams)

else:
    missingParams.append('EC_Engine')


# Write validation results
validation = {'missingParams': sorted(missingParams),
              'incorrectTypes': sorted(incorrectTypes)}
with open('rst.yml', 'w') as outfile:
    yaml.dump(validation, outfile, default_style=False)


# quite mode
if not args.quiet:
    print(validation)

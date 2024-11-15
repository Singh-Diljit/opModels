"""tech params"""

from collections import defaultdict

techs = {'FFT', 'Direct Integration', 'Closed Form',
         'MCM Process', 'MCM Direct', 'Lattice'}

tuningParams = defaultdict(set)
tuningParams = {'FFT': {'Dampening Function', 'Integral Discretization'},
                'Direct Integration': set(),
                'Closed Form': set(),
                'MCM Process': {'~dt', 'Simulations'},
                'MCM Direct': set(),
                'Lattice': {'Height'}}

stockParams = defaultdict(set)
stockParams = {'FFT': {'S', 'r', 'q'},
                'Direct Integration': {'S', 'r', 'q'},
                'Closed Form': set(),
                'MCM Process': {'dX'},
                'MCM Direct': {'S_t'},
                'Lattice': {'Height'}}

optionParams = defaultdict(set)
optionParams = {'FFT': {'phi', 'K', 'T', 'payOff'},
                'Direct Integration': {'phi', 'K', 'T', 'payOff'},
                'Closed Form': {'K', 'T', 'payOff'},
                'MCM Process': {'K', 'T', 'payOff'},
                'MCM Direct': {'K', 'T', 'payOff'},
                'Lattice': {'K', 'T', 'payOff'}}


techParams = defaultdict(set)
for tech in techs:
    techParams[tech].update(tuningParams[tech])
    techParams[tech].update(stockParams[tech])
    techParams[tech].update(optionParams[tech])

trackedParams = defaultdict(set)
for tech in techs:
    trackedParams['Stock'].update(stockParams[tech])
    trackedParams['Option'].update(optionParams[tech])

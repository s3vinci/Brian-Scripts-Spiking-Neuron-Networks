__author__ = 'Neuromanc3r'
from brian import *
'''
This is a simulation of many trials over one neuron which receives inhibitory and excitatory Poisson Input
Based on : R. Brette - Dec 2007
'''

N_trials = 100
# Time constants
taum=10*msecond
taue=5*msecond
taui=10*msecond

'''
Vogels2005 resting potential is -60 mV
'''
# Reversal potentials
Ee = (0. + 60.) * mvolt
Ei = (-80. + 60.) * mvolt

# Differential equations

eqs=Equations('''
dv/dt = (-v+ge*(Ee-v)+gi*(Ei-v))*(1./taum) : volt
dge/dt = -ge*(1./taue) : 1
dgi/dt = -gi*(1./taui) : 1
''')

# Create the Neuron Group with the specified number of trials
# I place the resting membrane potential at zero so that I don't have to deal with an extra variable
P = NeuronGroup(N_trials, model=eqs, threshold=10 * mvolt, \
              reset=0 * mvolt, refractory=5 * msecond,
              order=1, compile=True)

# Initialization
P.v = (randn(len(P)) * 5 - 5) * mvolt
P.ge = randn(len(P)) * 1.5 + 4
P.gi = randn(len(P)) * 12 + 20

# Initialize the Poisson Group

'''
Vogels2005 : figure 2e average firing rate approx 10 Hz
'''
F = 5*Hz
#initialize 200 ex and 50 inh poisson inputs for each trial
Pe = PoissonGroup(200*N_trials, rates=F)
Pi = PoissonGroup(50*N_trials,rates=F)

#how much stronger should the inhibitory current be than the excitatory one
'''
excitatory about 3 nS inhibitory conductance 55 nS
Vogels get a balance between excitation and inhibition
'''
we = 6./5.  # excitatory synaptic weight (voltage)
wi = 67./5. # inhibitory synaptic weight



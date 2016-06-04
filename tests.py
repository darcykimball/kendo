#!/usr/bin/python2

import time
import argparse

import kendo

def setup_parser():
    """Setup parser for reading parameters common to all tests
    
    Returns the arg parser
    """
    parser = argparse.ArgumentParser(description="Simulate threaded apps")
    parser.add_argument('--n_samples', metavar='MIN_INC', type=int, \
                                help='number of samples to collect for each \
                                set of parameters')
    parser.add_argument('--min_inc', metavar='MIN_INC', type=int, \
                                help='minimum logical time increment')
    parser.add_argument('--max_inc', metavar='MAX_INC', type=int, \
                                help='maximum logical time increment')
    parser.add_argument('--step_inc', metavar='STEP_INC', type=int, \
                                help='step amount for logical time increments \
                                between simulations')
    
    return parser

def run_varying_increments(arbitrator, min_inc, max_inc, step, n_samples):
    """Run a bunch of simulations varying logical time increments between
    threads.

    Returns a list of the results (priorities/time pairs)
    """

    times = []
    
    for priorities in permutationN(len(arbitrator.processes), min_inc, \
            max_inc, step):
        arbitrator.priorities = priorities

        print "*** Running threads with priorities = ", priorities, " ***"

        time_taken = 0
        for i in xrange(n_samples):
            begin = time.time()
            arbitrator.run()
            end = time.time()

            time_taken += end - begin

            arbitrator.reset()

        # Save the average
        times.append((priorities, time_taken/n_samples))     

    return times

def permutationN(n, min_val, max_val, step):
    for x in xrange(min_val, max_val, step):
        if n == 1:
            yield [x]
        else:
            for rest in permutationN(n - 1, min_val, max_val, step):
                yield rest + [x]

def seqFromGen(generators):
    if len(generators) == 1:
        for val in generators[0]:
            yield [val]
    else:
        for val in generators[0]:
            print 'val = ', val
            for rest in seqFromGen(generators[1:]):
                print 'rest = ', rest
                yield [val] + rest
        
def frange(min_val, max_val, step):
    while min_val < max_val:
        yield min_val
        min_val += step

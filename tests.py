#!/usr/bin/python2

import kendo
import argparse

def setup_parser():
    """Setup parser for reading parameters common to all tests
    
    Returns the arg parser
    """
    parser = argparse.ArgumentParser(description="Simulate threaded apps")
    parser.add_argument('min_inc', metavar='MIN_INC', type=int, \
                                help='minimum logical time increment')
    parser.add_argument('max_inc', metavar='MAX_INC', type=int, \
                                help='maximum logical time increment')
    parser.add_argument('step_inc', metavar='STEP_INC', type=int, \
                                help='step amount for logical time increments \
                                between simulations')
    
    return parser

def run_varying_increments(arbitrator, min_inc, max_inc, step):
    """Run a bunch of simulations varying logical time increments between
    threads.
    """
    
    for priorities in permutationN(len(arbitrator.processes), min_inc, \
            max_inc, step):
        arbitrator.priorities = priorities

        print "*** Running threads with priorities = ", priorities, " ***"
        arbitrator.run()
        


def permutationN(n, min_val, max_val, step):
    for x in xrange(min_val, max_val, step):
        if n == 1:
            yield [x]
        else:
            for rest in permutationN(n - 1, min_val, max_val, step):
                yield rest + [x]

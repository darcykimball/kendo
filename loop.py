#!/usr/bin/python2

import sys
import time
import itertools

class LoopProcess():
    """A simple process that alternates between doing independent work and
    being inside a critical section."""

    def __init__(self, arbitrator, lock_num, crit_time=0, work_time=0, \
            num_iterations=5, verbose=False):
        """Construct a LoopProcess.

        Args:
        arbitrator - the kendo (or other) arbitrator
        lock0_num  - number of the 1st lock used by this
        lock1_num  - number of the 2nd lock used by this
        """

        self.arbitrator = arbitrator
        self.lock_num = lock_num
        self.crit_time = crit_time
        self.work_time = work_time
        self.num_iterations = num_iterations
        self.verbose = verbose
        
        # FIXME: horrible dependencies; processes need their own pids...
        self.pid = arbitrator.register_process(self)

    def run(self):
        """Run this LoopProcess. Do work in a loop, entering a critical section
        repeatedly.
        """

        if self.verbose:
            print "LoopProcess, PID = ", self.pid, " starting..."

        for i in xrange(self.num_iterations):
            # Do work
            time.sleep(self.work_time)

            self.arbitrator.det_mutex_lock(self.pid, self.lock_num)

            if self.verbose:
                print "LoopProcess, PID = ", self.pid, \
                        " inside critical section..."
            time.sleep(self.crit_time)

            self.arbitrator.det_mutex_unlock(self.pid, self.lock_num)
                
        # FIXME: remove this after the scheduling's fixed
        self.arbitrator.clocks[self.pid] = 10000

        if self.verbose:
            print "LoopProcess, PID = ", self.pid, " done!"

def sanity_check():
    """A basic test"""

    print "Testing LoopProcess..."

    kendo_arbitrator = kendo.Kendo(max_processes=2, num_locks=2, debug=True, \
            priorities=[3,1])
    
    process1 = LoopProcess(kendo_arbitrator, 0, crit_time=0.5, work_time=1)
    process2 = LoopProcess(kendo_arbitrator, 0, crit_time=1, work_time=0.5)
    
    kendo_arbitrator.run()

    print "Done testing LoopProcess!"

if __name__ == "__main__":
    import kendo
    import tests
    
    if len(sys.argv) <= 1:
        sanity_check()
        sys.exit(0)

    # Get command-line args
    parser = tests.setup_parser()
    parser.add_argument('--n_threads', metavar='N_THREADS', type=int, \
            help='number of threads to use')
    parser.add_argument('--crit_times_min', metavar='CRIT_TIME_MIN', \
            type=float, nargs='+', \
            help='simulated critical section time, minimum value (sec)')
    parser.add_argument('--crit_times_max', metavar='CRIT_TIME_MAX', \
            type=float, nargs='+', \
            help='simulated critical section time, maximum value (sec)')
    parser.add_argument('--work_times_min', metavar='WORK_TIME_MIN', \
            type=float, nargs='+', \
            help='simulated work time, minimum value (sec)')
    parser.add_argument('--work_times_max', metavar='WORK_TIME_MAX', \
            type=float, nargs='+', \
            help='simulated work time, maximum value (sec)')
    parser.add_argument('--work_time_step', metavar='WORK_TIME_STEP', \
            type=float, help='work time step')
    parser.add_argument('--crit_time_step', metavar='CRIT_TIME_STEP', \
            type=float, help='critical section time step') 

    args = parser.parse_args()

    if args.work_times_min is not None and args.crit_times_min is not None:
        assert len(args.work_times_min) == args.n_threads == \
                len(args.crit_times_max) == len(args.crit_times_min) == \
                len(args.work_times_max)
    else:
        args.work_times_min = [0.0 for i in xrange(args.n_threads)]
        args.crit_times_min = [0.0 for i in xrange(args.n_threads)]
        args.work_times_max = [1.0 for i in xrange(args.n_threads)]
        args.crit_times_max = [1.0 for i in xrange(args.n_threads)]
        args.work_time_step = 0.5
        args.crit_time_step = 0.5   

    # Setup ranges for critical section/work times
    work_time_generators = \
            [tests.frange(args.work_times_min[i], args.work_times_max[i], \
            args.work_time_step) for i in xrange(args.n_threads)]
    crit_time_generators = \
            [tests.frange(args.crit_times_min[i], args.crit_times_max[i], \
            args.crit_time_step) for i in xrange(args.n_threads)]

    # Setup simulations
    for work_times in itertools.product(*work_time_generators):
        for crit_times in itertools.product(*crit_time_generators):
            print "work_times = ", work_times
            print "crit_times = ", crit_times

            kendo_arbitrator = kendo.Kendo(max_processes=args.n_threads, \
                    num_locks=1, \
                    debug=False)

            processes = []
            for i in xrange(args.n_threads):
                processes.append(LoopProcess(kendo_arbitrator, 0, \
                        crit_time=crit_times[i], \
                        work_time=work_times[i]))

            times = tests.run_varying_increments(kendo_arbitrator, \
                    args.min_inc, \
                    args.max_inc, args.step_inc, args.n_samples)

            print "Result times:"
            for p, t in times:
                print p, t


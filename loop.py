#!/usr/bin/python2

import time

class LoopProcess():
    """A simple process that simulates nested locking."""

    def __init__(self, arbitrator, lock_num, crit_time=0, work_time=0, num_iterations=3):
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
        
        # FIXME: horrible dependencies; processes need their own pids...
        self.pid = arbitrator.register_process(self)

    def run(self):
        """Run this LoopProcess. Do work in a loop, entering a critical section
        repeatedly.
        """

        print "LoopProcess, PID = ", self.pid, " starting..."

        for i in xrange(self.num_iterations):
            # Do work
            time.sleep(self.work_time)

            self.arbitrator.det_mutex_lock(self.pid, self.lock_num)

            print "LoopProcess, PID = ", self.pid, " inside critical section..."
            time.sleep(self.crit_time)

            self.arbitrator.det_mutex_unlock(self.pid, self.lock_num)
                
        # FIXME: remove this after the scheduling's fixed
        self.arbitrator.clocks[self.pid] = 10000

        print "LoopProcess, PID = ", self.pid, " done!"

if __name__ == "__main__":
    import kendo

    print "Testing LoopProcess..."

    kendo_arbitrator = kendo.Kendo(max_processes=2, num_locks=2, debug=True, \
            priorities=[3,1])
    
    process1 = LoopProcess(kendo_arbitrator, 0, crit_time=0.5, work_time=1)
    process2 = LoopProcess(kendo_arbitrator, 0, crit_time=1, work_time=0.5)
    
    kendo_arbitrator.run()

    print "Done testing LoopProcess!"

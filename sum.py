#!/usr/bin/python2

import random
import time

class SumProcess():
    """A thread that computes part of a sum."""

    def __init__(self, arbitrator, lock_num, nums, delay_time=0, work_time=0):
        """Construct a SumProcess.

        Args:
        arbitrator - the kendo (or other) arbitrator
        lock_num - lock protecting shared sum
        nums - iterable of numbers to addup
        delay_time - time to delay before starting work
        work_time - simulated time it takes to complete the work
        """

        self.arbitrator = arbitrator
        self.lock_num = lock_num
        self.nums = nums
        self.delay_time = delay_time
        self.work_time = work_time

        # Initialize the shared memory total
        # XXX: this is redundant since multiple threads will do this, but it's
        # OK since this is just for initialization before anything runs
        arbitrator.mutate_shared("total_sum", 0)
        
        # FIXME: horrible dependencies; processes need their own pids...
        self.pid = arbitrator.register_process(self)

    def run(self):
        """Run this SumProcess. Add up its numbers and update the total when
        done.
        """

        # Delay a bit.
        time.sleep(self.delay_time)

        print "SumProcess, PID = ", self.pid, " starting..."

        # Do the calculation
        local_total = sum(self.nums)

        # Simulate time-consuming work
        time.sleep(self.work_time)

        print "SumProcess, PID = ", self.pid, "local_total = ", local_total

        # Update the total in shared memory
        self.arbitrator.det_mutex_lock(self.pid, self.lock_num)

        print "SumProcess, PID = ", self.pid, "total_sum before = ", self.arbitrator.shared_mem["total_sum"]
        self.arbitrator.shared_mem["total_sum"] += local_total
        print "SumProcess, PID = ", self.pid, "total_sum after = ", self.arbitrator.shared_mem["total_sum"]

        self.arbitrator.det_mutex_unlock(self.pid, self.lock_num)
                
        # FIXME: remove this after the scheduling's fixed
        self.arbitrator.clocks[self.pid] = 10000

        print "SumProcess, PID = ", self.pid, " done!"

if __name__ == "__main__":
    import kendo

    print "Testing SumProcess..."
    
    priorities = [4,3,2,1]
    kendo_arbitrator = kendo.Kendo(max_processes=4, num_locks=1, debug=True, \
        priorities=priorities)

    process1 = SumProcess(kendo_arbitrator, 0, xrange(10000), work_time=random.random())
    process2 = SumProcess(kendo_arbitrator, 0, xrange(10000, 20000), work_time=random.random())
    process3 = SumProcess(kendo_arbitrator, 0, xrange(20000, 30000), work_time=random.random())
    process4 = SumProcess(kendo_arbitrator, 0, xrange(30000, 40000), work_time=random.random())
    
    kendo_arbitrator.run()

    print "Done testing SumProcess!"

    print "Result = ", kendo_arbitrator.shared_mem

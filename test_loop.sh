#!/bin/bash -e

./loop.py --min_inc 1 --max_inc 6 --step_inc 1 --n_threads 2 \
        --work_times_min 0.0001 0.0001 --work_times_max 0.001 0.001 \
        --crit_times_min 0.0001 0.0001 --crit_times_max 0.001 0.001 \
        --work_time_step 0.0004  --crit_time_step 0.0004 --n_samples 3

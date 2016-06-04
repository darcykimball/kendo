#!/usr/bin/python2

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from mpl_toolkits.mplot3d import Axes3D
import argparse

parser = argparse.ArgumentParser(description="Analyze/plot run data")
parser.add_argument('input_data', metavar='data.csv', type=str, \
        help='input data file, in csv format')

args = parser.parse_args()

df = pd.read_csv(args.input_data)

for i in df.columns:
    df[i] = df[i].astype(float)

# Lowest crit/work times, even load
lo_p1_inc = df[:26]['P1 inc']
lo_p2_inc = df[:26]['P2 inc']
lo_times = df[:26]['time']

# Highest cirt/work times, even load
hi_p1_inc = df[-25:]['P1 inc']
hi_p2_inc = df[-25:]['P2 inc']
hi_times = df[-25:]['time']

# Highest cirt/work times,very uneven load
uneven_p1_inc = df[601:627]['P1 inc']
uneven_p2_inc = df[601:627]['P2 inc']
uneven_times = df[601:627]['time']

# Highest cirt/work times, moderately uneven load
med_uneven_p1_inc = df[1302:1328]['P1 inc']
med_uneven_p2_inc = df[1302:1328]['P2 inc']
med_uneven_times = df[1302:1328]['time']


fig = plt.figure()
fig.set_size_inches(12, 8)
ax_lo = fig.add_subplot(221, projection='3d')
ax_lo.set_title('No load difference, short')
ax_lo.set_xlabel('P1 increment (s)')
ax_lo.set_ylabel('P2 increment (s)')
ax_lo.set_zlabel('Time (s)')
ax_lo.xaxis._axinfo['label']['space_factor'] = 3
ax_lo.yaxis._axinfo['label']['space_factor'] = 3
ax_lo.zaxis._axinfo['label']['space_factor'] = 3
ax_lo.zaxis._axinfo['ticklabel']['space_factor'] = 1.5
ax_lo.view_init(15, 120)
    
ax_hi = fig.add_subplot(222, projection='3d')
ax_hi.set_title('No load difference, long')
ax_hi.set_xlabel('P1 increment (s)')
ax_hi.set_ylabel('P2 increment (s)')
ax_hi.set_zlabel('Time (s)')
ax_hi.xaxis._axinfo['label']['space_factor'] = 3
ax_hi.yaxis._axinfo['label']['space_factor'] = 3
ax_hi.zaxis._axinfo['label']['space_factor'] = 3
ax_hi.zaxis._axinfo['ticklabel']['space_factor'] = 1.5
ax_hi.view_init(15, 120)

ax_uneven = fig.add_subplot(223, projection='3d')
ax_uneven.set_title('Large load difference')
ax_uneven.set_xlabel('P1 increment (s)')
ax_uneven.set_ylabel('P2 increment (s)')
ax_uneven.set_zlabel('Time (s)')
ax_uneven.xaxis._axinfo['label']['space_factor'] = 3
ax_uneven.yaxis._axinfo['label']['space_factor'] = 3
ax_uneven.zaxis._axinfo['label']['space_factor'] = 3
ax_uneven.zaxis._axinfo['ticklabel']['space_factor'] = 1.5
ax_uneven.view_init(15, 120)

ax_uneven_mid = fig.add_subplot(224, projection='3d')
ax_uneven_mid.set_title('Medium load difference')
ax_uneven_mid.set_xlabel('P1 increment (s)')
ax_uneven_mid.set_ylabel('P2 increment (s)')
ax_uneven_mid.set_zlabel('Time (s)')
ax_uneven_mid.xaxis._axinfo['label']['space_factor'] = 3
ax_uneven_mid.yaxis._axinfo['label']['space_factor'] = 3
ax_uneven_mid.zaxis._axinfo['label']['space_factor'] = 3
ax_uneven_mid.zaxis._axinfo['ticklabel']['space_factor'] = 1.5
ax_uneven_mid.view_init(15, 120)

ax_lo.scatter(lo_p1_inc, lo_p2_inc, lo_times)
ax_hi.scatter(hi_p1_inc, hi_p2_inc, hi_times)
ax_uneven.scatter(uneven_p1_inc, uneven_p2_inc, uneven_times)
ax_uneven_mid.scatter(med_uneven_p1_inc, med_uneven_p2_inc, med_uneven_times)

#fig.show()
pylab.savefig("runs_plots.png")

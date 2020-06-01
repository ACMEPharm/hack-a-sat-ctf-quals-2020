#!/usr/bin/env python3

import argparse
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("signal_data", type=argparse.FileType("rb"))
parser.add_argument("--channel", type=int, default=0)
parser.add_argument("--sample_rate", type=int, default=102400)
parser.add_argument("--time_slice", type=float)
parser.add_argument("--offset", type=int, default=0)
args = parser.parse_args()

def file_size(fp):
    cur = fp.tell()
    fp.seek(0, 2)
    size = fp.tell()
    fp.seek(cur)
    return size

if args.time_slice == None:
    count = file_size(args.signal_data) // 4
else:
    count = int(args.sample_rate * args.time_slice) * 2

signals = np.fromfile(args.signal_data, dtype=np.float32, count=count, sep="", offset=int(args.offset * args.sample_rate))

if args.channel == 0:
    signals = signals[::2]
else:
    signals = signals[1::2]

plt.plot(signals)
plt.show()

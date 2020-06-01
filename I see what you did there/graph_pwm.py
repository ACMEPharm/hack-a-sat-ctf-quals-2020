#!/usr/bin/env python3

import argparse
import os

import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument("training_datas", type=argparse.FileType("rb"), nargs="+")
parser.add_argument("--samples_per_clock", type=float, default=2048)
parser.add_argument("--threshold", type=float, default=-60)
parser.add_argument("--num_checks", type=int, default=10)
args = parser.parse_args()

THRESHOLD = args.threshold
SAMPLES_PER_CYCLE = args.samples_per_clock

def file_size(fp):
    return os.fstat(fp.fileno()).st_size

def calc_pwm_for_cycle(samples, cycle):
    def count_peak_cycles(data, index):
        # find the first peak
        count = 0
        while data[count][index] < THRESHOLD:
            count += 1

        # save this point
        start = count
        
        # advance until this peak goes down
        while data[count][index] > THRESHOLD:
            count += 1

        # find the next peak
        while data[count][index] < THRESHOLD:
            count += 1
        
        # this should be the count of the number of cyles the PWM signal was "on"
        return count - start
    
    # clocks drift/not exactly aligned so we start counting a bit before where we expect the start of the PWM cycle
    i = cycle * SAMPLES_PER_CYCLE
    start = i if i == 0 else i - 100
    tmp_samples = samples[start:i+SAMPLES_PER_CYCLE]

    azimuth_on_cycles = count_peak_cycles(tmp_samples, 0)
    elevation_on_cycles = count_peak_cycles(tmp_samples, 1)

    return (azimuth_on_cycles/SAMPLES_PER_CYCLE, elevation_on_cycles/SAMPLES_PER_CYCLE)


def pwm_iter(signal_file):
    samples = np.fromfile(signal_file, dtype=np.dtype((np.float32, 2)), count=file_size(signal_file) // 8, sep="")
    for i in range(0, len(samples) // SAMPLES_PER_CYCLE):
        yield calc_pwm_for_cycle(samples, i)

def plot_pwm(signal_file, ax):
    azimuths_rf = []
    elevations_rf = []

    for azimuth_avg_rf, elevation_avg_rf in pwm_iter(signal_file):
        print("Azimuth:", azimuth_avg_rf, "Elevation:", elevation_avg_rf)

        azimuths_rf.append(azimuth_avg_rf)
        elevations_rf.append(elevation_avg_rf)
    
    ax.plot(azimuths_rf)
    ax.plot(elevations_rf)
    #ax.set_title(signal_file.filename)

if len(args.training_datas) > 1:
    fig, axes = plt.subplots(1, len(args.training_datas))
    for data_fd, ax in zip(args.training_datas, axes):
        plot_pwm(data_fd, ax)
else:
    plot_pwm(args.training_datas[0], plt)

plt.show()

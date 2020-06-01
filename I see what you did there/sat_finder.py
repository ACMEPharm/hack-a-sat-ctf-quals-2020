#!/usr/bin/env python3

import argparse
import numpy as np
import mmap
import random
import datetime
import collections
import os

import skyfield.api as sf

parser = argparse.ArgumentParser()
parser.add_argument("db", help="Database of TLE data for satellites")
parser.add_argument("signal_file", type=argparse.FileType("rb"), help="Captured radio emissions from the motor cables")
parser.add_argument("latitude", type=float, help="Ground location's latitude")
parser.add_argument("longitude", type=float, help="Ground location's latitude")
parser.add_argument("time", type=float, help="The time the recording was made")
parser.add_argument("--sample_rate", type=float, default=102400, help="Sample rate of the signal data")
parser.add_argument("--samples_per_cycle", type=float, default=2048, help="Number of samples per PWM cycle")
parser.add_argument("--threshold", type=float, default=-60, help="Threshold to identify the peaks")
parser.add_argument("--num_checks", type=int, default=10, help="How many time offsets to use")
parser.add_argument("--error", type=float, default=0.02, help="The allowed error rate betwe recovred and caculated PWM")
args = parser.parse_args()

# Starfield Globals
SATELLITES = sf.load.tle_file(args.db)
GROUND_CONTROL = sf.Topos(latitude_degrees=args.latitude, longitude_degrees=args.longitude)
ts = sf.load.timescale()

# Configuration data
THRESHOLD = args.threshold
SAMPLES_PER_CYCLE = args.samples_per_cycle
TIME_PER_CYCLE = SAMPLES_PER_CYCLE / args.sample_rate
PWM_MIN = 0.03  # from the README.txt
PWM_MAX = 0.35

# read in all the samples
def file_size(fp):
    return os.fstat(fp.fileno()).st_size

samples = np.fromfile(args.signal_file, dtype=np.dtype((np.float32, 2)), count=file_size(args.signal_file) // 8, sep="")
NUM_CYCLES = len(samples) // SAMPLES_PER_CYCLE

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
    
    # clock drift/not exactly aligned so we start counting a bit before where we expect the start of the PWM cycle
    i = cycle * SAMPLES_PER_CYCLE
    start = i if i == 0 else i - 100
    tmp_samples = samples[start:i+SAMPLES_PER_CYCLE]

    azimuth_on_cycles = count_peak_cycles(tmp_samples, 0)
    elevation_on_cycles = count_peak_cycles(tmp_samples, 1)

    return (azimuth_on_cycles/SAMPLES_PER_CYCLE, elevation_on_cycles/SAMPLES_PER_CYCLE)

def sat_cal_az_el(sat, t):
    # create a vector between sat and ground control
    diff = sat - GROUND_CONTROL

    # convert time to a SF time object
    t = ts.utc(datetime.datetime.fromtimestamp(t, datetime.timezone.utc))

    # calculate our position
    topocentric = diff.at(t)

    # convert to degrees
    el, az, distance = topocentric.altaz()

    return az.degrees, el.degrees

def to_pwm(deg):
    return PWM_MIN + (PWM_MAX - PWM_MIN) * (deg / 180.0)

def sat_calc_pwm(sat, t):
    az, el = sat_cal_az_el(sat, t)

    if az > 180:
        az = az - 180
        el = 180 - el
    
    return to_pwm(az), to_pwm(el)

def should_filter_sat(sat, azimuth_pwm, elevation_pwm, t, error):
    az, el = sat_calc_pwm(sat, t)

    return abs(az - azimuth_pwm) < error and \
        abs(el - elevation_pwm) < error

seen_stats = collections.Counter()
for i in range(args.num_checks):
    cycle = random.randint(0, NUM_CYCLES - 1)
    t = args.time + cycle * TIME_PER_CYCLE
    azimuth_pwm_signal, elevation_pwm_signal = calc_pwm_for_cycle(samples, cycle)
    print("Signal Cycle:", cycle, "Time:", t)
    print("\tAzimuth:", azimuth_pwm_signal)
    print("\tElevation:", elevation_pwm_signal)

    sats = filter(lambda sat: should_filter_sat(sat, azimuth_pwm_signal, elevation_pwm_signal, t, args.error), SATELLITES)
    seen_stats.update(map(lambda sat: sat.name, sats))
    print("\tCurrent Stats:", ", ".join(map(lambda x: f"{x[0]} ({x[1]})", seen_stats.most_common())))

print()
print("Final stats")
print("="*20)
for name, count in seen_stats.most_common():
    print(f"{name} ({count})")

#!/usr/bin/env python3

import argparse
import binascii

parser = argparse.ArgumentParser()
parser.add_argument("input", type=argparse.FileType("r"))
parser.add_argument("output", type=argparse.FileType("wb"))
args = parser.parse_args()

out_fd = args.output

for l in args.input:
    comps = l.split("\t")

    if len(comps) < 2:
        continue

    offset = comps[0].strip()
    if len(offset) == 0:
        continue

    if offset[-1] != ':':
        # not an instruction line...
        continue

    offset = int(offset[:-1], 16)

    data = comps[1].strip().replace(" ", "")
    try:
        data = binascii.unhexlify(data)
    except:
        print("Failed to decode:", hex(offset), data)
        continue

    out_fd.seek(offset)
    out_fd.write(data)

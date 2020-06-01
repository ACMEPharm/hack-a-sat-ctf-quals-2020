#!/usr/bin/env python3

import argparse
import numpy
import binascii
import struct

COORDS_OFFSET = 0x3f0
COORDS_OFFSET_PC = COORDS_OFFSET // 4
COORDS_SIZE = 4 * 4 * 2
COORDS_SIZE_PC = COORDS_SIZE // 4
CHECKSUM_OFFSET = COORDS_OFFSET + COORDS_SIZE
CHECKSUM_OFFSET_PC = CHECKSUM_OFFSET // 4
CHECKSUM_SIZE = 16
CHECKSUM_SIZE_PC = CHECKSUM_SIZE // 4
OUTPUT_OFFSET = 0x244
OUTPUT_OFFSET_PC = OUTPUT_OFFSET // 4
OUTPUT_SIZE = 0x2c
OUTPUT_SIZE_PC = OUTPUT_SIZE // 4

parser = argparse.ArgumentParser()
parser.add_argument("op_input", type=argparse.FileType("rb"))
args = parser.parse_args()

def hexlify(d):
    return str(binascii.hexlify(d), "ascii").upper()

op_data = bytearray(args.op_input.read())
op_int = numpy.frombuffer(op_data, dtype=numpy.int32)

op_int[0x00000107] = 0xe6

pc = op_int[-1]
step_count = 0
while pc < len(op_int):
    op0, op1, op2, op3 = op_int[pc:pc+4]
    step_count += 1

    #if op2 in (OUTPUT_OFFSET_PC, 0x20):
    #    print("PC = {:08x}({:08x}) OP: {:08x} {:08x} {:08x} {:08x}".format(pc, pc*4, op0, op1, op2, op3))

    if op2 == 0xffffffff and op1 == 0xffffffff and op0 == 0xffffffff:
        print("Stop instruction?")
        break

    op_int[op2] = op_int[op2] + op_int[op1]
    #print("\top[{:08x}] = op[{:08x}] + op[{:08x}]".format(op2, op2, op1))
    
    if  (op_int[op1] >= 0 and op_int[op2] <= op_int[op0]) or \
        (op_int[op1] < 0 and op_int[op2] >= op_int[op0]):
        pc = pc + op3
    else:
        pc = pc + 4

print(f"Ran for {step_count} steps")
print("Output:", hexlify(op_data[OUTPUT_OFFSET:OUTPUT_OFFSET+OUTPUT_SIZE:4]))
checksum = op_data[CHECKSUM_OFFSET:CHECKSUM_OFFSET + CHECKSUM_SIZE]
checksum = struct.pack(">IIII", *struct.unpack("<IIII", checksum))
print("CMD: ADCS CFG_POS {:08x} {:08x} {}".format(0, 0, hexlify(checksum)))

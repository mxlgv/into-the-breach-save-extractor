#!/usr/bin/env python3

# SPDX-License-Identifier: GPL-2.0-only
# Copyright (C) 2026 Maxim Logaev <maxlogaev@proton.me>

# Netflix cloud save file extractor
# for the Android version of the game "Into the Breach".

import os
import sys
import zlib


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def extract_file(fd, out_dir, f_item):

    dir = os.path.join(out_dir, "profile_" + str(f_item[0]))

    if not os.path.exists(dir):
        os.mkdir(dir)

    out_fname = os.path.join(dir, f_item[1])

    print(f" {out_fname}: ", end='')

    compr_data = fd.read(f_item[2])

    decompr_data = zlib.decompress(compr_data)
    with open(out_fname, 'wb') as out_file:
        out_file.write(decompr_data)

    print("OK")


def main(argv):
    ex_files = []

    if len(argv) < 2:
        eprint("Usage: python3 itb-save-extract.py <input.slot> <output_dir>")
        return 1

    in_file = argv[1]
    out_dir = argv[2]

    if not os.path.isdir(out_dir):
        eprint(f"Output directory \"{out_dir}\" not found")
        return 1

    # Read cloud save file
    with open(in_file, 'rb') as slot_file:

        # Validate magic "SLOT"
        bytes = slot_file.read(0x4)
        if (bytes != b'\x53\x4C\x4F\x54'):
            eprint(f"File \"{in_file}\" is not the Netflix cloud save file "
                   "for \"Into the Breach\"!")
            return 1

        # Skip unknown
        slot_file.seek(0x8, os.SEEK_CUR)

        # Read date0. TODO: Find out why this date is needed.
        bytes = slot_file.read(0x18)
        print("Date0: " + bytes.decode('utf-8'))

        # Skip unknown
        slot_file.seek(0x12, os.SEEK_CUR)

        bytes = slot_file.read(0x24)
        print("UUID: " + bytes.decode('utf-8'))

        # Skip unknown
        slot_file.seek(0x8, os.SEEK_CUR)

        # Read date1. TODO: Find out why this date is needed.
        bytes = slot_file.read(0x18)
        print("Date1: " + bytes.decode('utf-8'))

        # Skip newline date byte
        slot_file.seek(0x1, os.SEEK_CUR)

        # Read number of files
        bytes = slot_file.read(0x4)
        num_files = int.from_bytes(bytes, "little")
        print(f"Contains {num_files} files (compressed size):")

        prof_id = -1

        for i in range(num_files):

            # Read file name
            bytes = slot_file.read(0x4)
            fname_len = int.from_bytes(bytes, "little")

            bytes = slot_file.read(fname_len)
            fname = bytes.decode('utf-8')

            if (fname == "profile.lua"):
                prof_id += 1
                print(f" profile_{prof_id}:")

            # Skip unknown
            slot_file.seek(0xC, os.SEEK_CUR)

            bytes = slot_file.read(0x4)
            compr_size = int.from_bytes(bytes, "little")

            print(f"   {fname}: {compr_size} bytes")

            ex_files.append((prof_id, fname, compr_size))

            # Skip unknown
            slot_file.seek(0x4, os.SEEK_CUR)

        if (prof_id < 0):
            eprint(f"File \"profile.lua\" not found in \"{in_file}\"!")
            return 1

        print("Extracting files: ")

        for f_item in ex_files:
            extract_file(slot_file, out_dir, f_item)

        print("Done")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

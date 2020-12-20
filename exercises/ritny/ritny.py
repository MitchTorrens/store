#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""'Ring in the New Year' Solution (by Mitch Torrens)

Implements the following algorithm and its inverse (from the similarly named
puzzle posted by Google in Dec 2020):

1. Start with the input string (Input)
2. append an end marker ($)
3. take the word and rotate it by moving the first character to the end.
4. add each rotation to a table and repeat (3) until you get back to the
   original order (Rotation table)
5. sort the rotations, with the end marker sorting to the end (Sort table)
6. take the final column as the output (Output)

Example:
    'anagram' -> 'nr$aaagm'

Note: Step 5 and the associated sort instructions were interpreted to mean that
the marker is always sorted last. Another possible interpretation would involve
sorting the marker normally (ascii value), instead manually moving the last
element of the Rotation table to the end of the Sort table. This assumption only
affects the intermediate Sort table state, and only in specific cases (excluding
the two provided examples).
"""

from argparse import ArgumentParser, RawTextHelpFormatter
from textwrap import dedent
import sys
import logging


logging.basicConfig(
    format='%(message)s'
)

_MARKER = chr(0x10ffff) # str character upper limit

__all__ = ['mark_and_rotate', 'sort', 'last_chars', 'decode', 'encode']


def mark_and_rotate(in_string, marker):
    """Append end marker to input and generate Rotation table."""
    in_string += marker
    return [in_string[i:] + in_string[:i] for i in range(len(in_string))]


def sort(rotation_table, marker):
    """Generate Sort table from Rotation table."""
    assert not any(_MARKER in s for s in rotation_table)
    # Substitution eliminates need for str overriding/subclassing/wrapping
    sorted_table = sorted([s.replace(marker, _MARKER) for s in rotation_table])
    return [s.replace(_MARKER, marker) for s in sorted_table]


def last_chars(sort_table):
    """Append end marker and generate rotation table."""
    return ''.join([s[-1] for s in sort_table])


def encode(in_string, marker):
    """Generate encoded string (run all steps of the encoding algorithm)."""
    return last_chars(sort(mark_and_rotate(in_string, marker), marker))


def decode(coded_string, marker):
    """Reverse encoding algorithm: Generates original input from encoded output."""
    assert coded_string.count(_MARKER) == 0
    if coded_string.count(marker) != 1:
        raise ValueError(f"Only messages with exactly one marker character '{marker}' can be decoded.")

    sortable_string = coded_string.replace(marker, _MARKER)
    last_column = list(sortable_string)
    first_column = sorted(last_column)

    adjacent_chars = []
    edge_lookup = dict()
    key = None
    for i, f in enumerate(first_column):
        adjacent_chars.append([last_column[i], f])
        edge_lookup.setdefault(last_column[i], []).append(i)

    edge_indices = [None] * len(first_column)
    prev_key = None
    for left_index, left_key in enumerate(adjacent_chars):
        if left_key[1] != prev_key:
            prev_key = left_key[1]
            ordered_char_mapping = iter(edge_lookup[left_key[1]])
        edge_indices[left_index] = next(ordered_char_mapping)

    node_index = last_column.index(_MARKER)
    decoded_sequence = []
    for i in range(len(edge_indices)):
        decoded_sequence.append(adjacent_chars[node_index][1])
        node_index = edge_indices[node_index]

    return ''.join(c for c in decoded_sequence).rstrip(_MARKER)


def main(argv):
    """
    'Ring in the New Year' puzzle solution: string encoding/decoding utility.

    Individually processes a list of 'passwords', decoding those containining
    a 'marker' character and encoding the rest, using an algorithm implemented
    to solve the above-named puzzle.

    HINT: Enclose each password in single quotes when running from a shell.
    """
    parser = ArgumentParser(
        description=dedent(main.__doc__),
        formatter_class=lambda prog: RawTextHelpFormatter(prog, max_help_position=30))
    parser.add_argument('passwords', nargs='*', type=str, metavar='password',
        help="List of strings to encode/decode.")
    parser.add_argument('-v', '--verbose', action='store_true', help='Show verbose output (intermediate states)')
    parser.add_argument('-m', '--marker', type=str, default='$', help="Marker character [default: '$']")
    args = parser.parse_args(argv)

    log = logging.getLogger()
    log.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    if len(args.marker) != 1:
        log.warn(f"{parser.prog}: Provided marker must be a single character.")
        parser.print_help()
        return 2

    if len(args.passwords) == 0:
        log.warn("No password(s) provided to encode/decode!\n")
        parser.print_help()
        log.info("\nPreviewing encoder/decoder with default examples...\n" + \
            f"$ ./ritny.py 'anagram' 'endrtednedd:/os....cp.rnnn.rhhps/.tt{args.marker}sfeaiaaofd.ow.otooapa.asu./thhse'")
        args.passwords = ['anagram', f'endrtednedd:/os....cp.rnnn.rhhps/.tt{args.marker}sfeaiaaofd.ow.otooapa.asu./thhse']

    log.debug(f"Using marker: '{args.marker}'...\n")
    outputs = []
    for password in args.passwords:
        if args.marker in password:
            log.debug(f"Decoding:\n {password}")
            output = decode(password, args.marker)
            outputs.append(output)
            log.debug(f"Decoded:\n {output}\n")

        else:
            log.debug(f"Encoding:\n {password}")

            rotation_table = mark_and_rotate(password, args.marker)
            rotation_display = '\n '.join(s for s in rotation_table)
            log.debug(f"Rotation table:\n {rotation_display}")

            sorted_table = sort(rotation_table, args.marker)
            sort_display = '\n '.join(s for s in sorted_table)
            log.debug(f"Sort table:\n {sort_display}")

            output = last_chars(sorted_table)
            log.debug(f"Encoded:\n {output}\n")
            outputs.append(output)

    log.info(' '.join(o for o in outputs))

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

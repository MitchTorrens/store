#!/usr/bin/env python3
"""'Ring in the New Year' (ritny) - Tests"""

import ritny

from collections import namedtuple
import unittest
import logging
import sys
import string
import random


log = logging.getLogger()


class TestRITNY_Unit(unittest.TestCase):
    TestArgs = namedtuple('TestArgs', 'marker password rotation_table sorted_table output')
    test_cases = [
        TestArgs(
            '$',
            'anagram',
            [
                'anagram$',
                'nagram$a',
                'agram$an',
                'gram$ana',
                'ram$anag',
                'am$anagr',
                'm$anagra',
                '$anagram',
            ], [
                'agram$an',
                'am$anagr',
                'anagram$',
                'gram$ana',
                'm$anagra',
                'nagram$a',
                'ram$anag',
                '$anagram',
            ],
            'nr$aaagm',
        ),
        TestArgs(
            '$',
            'mitchtorrens@gmail.com',
            [
                'mitchtorrens@gmail.com$',
                'itchtorrens@gmail.com$m',
                'tchtorrens@gmail.com$mi',
                'chtorrens@gmail.com$mit',
                'htorrens@gmail.com$mitc',
                'torrens@gmail.com$mitch',
                'orrens@gmail.com$mitcht',
                'rrens@gmail.com$mitchto',
                'rens@gmail.com$mitchtor',
                'ens@gmail.com$mitchtorr',
                'ns@gmail.com$mitchtorre',
                's@gmail.com$mitchtorren',
                '@gmail.com$mitchtorrens',
                'gmail.com$mitchtorrens@',
                'mail.com$mitchtorrens@g',
                'ail.com$mitchtorrens@gm',
                'il.com$mitchtorrens@gma',
                'l.com$mitchtorrens@gmai',
                '.com$mitchtorrens@gmail',
                'com$mitchtorrens@gmail.',
                'om$mitchtorrens@gmail.c',
                'm$mitchtorrens@gmail.co',
                '$mitchtorrens@gmail.com',
            ], [
                '.com$mitchtorrens@gmail',
                '@gmail.com$mitchtorrens',
                'ail.com$mitchtorrens@gm',
                'chtorrens@gmail.com$mit',
                'com$mitchtorrens@gmail.',
                'ens@gmail.com$mitchtorr',
                'gmail.com$mitchtorrens@',
                'htorrens@gmail.com$mitc',
                'il.com$mitchtorrens@gma',
                'itchtorrens@gmail.com$m',
                'l.com$mitchtorrens@gmai',
                'mail.com$mitchtorrens@g',
                'mitchtorrens@gmail.com$',
                'm$mitchtorrens@gmail.co',
                'ns@gmail.com$mitchtorre',
                'om$mitchtorrens@gmail.c',
                'orrens@gmail.com$mitcht',
                'rens@gmail.com$mitchtor',
                'rrens@gmail.com$mitchto',
                's@gmail.com$mitchtorren',
                'tchtorrens@gmail.com$mi',
                'torrens@gmail.com$mitch',
                '$mitchtorrens@gmail.com'
            ],
            'lsmt.r@camig$oectronihm',
    )]

    def test_rotate(self):
        for case in self.test_cases:
            self.assertListEqual(ritny.mark_and_rotate(case.password, case.marker), case.rotation_table)

    def test_sort(self):
        for case in self.test_cases:
            self.assertListEqual(ritny.sort(case.rotation_table, case.marker), case.sorted_table)

    def test_last_chars(self):
        for case in self.test_cases:
            self.assertEqual(ritny.last_chars(case.sorted_table), case.output)

    def test_decode(self):
        for case in self.test_cases:
            self.assertEqual(ritny.decode(case.output, case.marker), case.password)


class TestRITNY_Algorithm(unittest.TestCase):
    random_charset = string.ascii_letters + string.digits + string.punctuation
    input_lengths = [0, 1, 2, 20, 400]

    def test_reversible(self):
        log.info(f'-> {len(self.input_lengths)} randomly generated test cases:')

        for i, input_length in enumerate(self.input_lengths):
            marker = random.choice(self.random_charset)
            test_string = ''.join(random.choices(self.random_charset.replace(marker, ''), k=input_length))
            log.info(f"  testing '{test_string}' with marker '{marker}'")

            encoded = ritny.encode(test_string, marker)
            decoded = ritny.decode(encoded, marker)
            self.assertEqual(test_string, decoded)


def main():
    args = sys.argv[1:]
    if '-q' not in args and '--quiet' not in args and ('-v' in args or '--verbose' in args):
        log.setLevel(logging.INFO)
    unittest.main()


if __name__ == '__main__':
    main()

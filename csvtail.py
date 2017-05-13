#!/usr/bin/env python

from argparse import ArgumentParser
import sys


DESCRIPTION = 'csvtail - prints header and last lines of input.'
EXAMPLES = 'example: cat file.csv | csvtail -n -100 skip first 100 rows and print file.csv till the end.'

def main(args):
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'w') if args.output_file else sys.stdout

    output_stream.write(input_stream.readline())
    if args.rows_count < 0:
	for _ in range(-args.rows_count):
            input_stream.readline()
        for row in input_stream:
            output_stream.write(row)
    else:
        lines = input_stream.readlines()
        for line in lines[(len(lines) - args.rows_count):]:
            output_stream.write(line)

    if input_stream != sys.stdin:
        input_stream.close()
    if output_stream != sys.stdout:
        output_stream.close()


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-n', '--rows_count', type=int,
                        help='Number of last rows to print if positive ROWS_COUNT.\
                        Else skips ROWS_COUNT lines and prints till the end of input.',
                        default=100)
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')

    parser.add_argument('file', nargs='?', help='File to read input from.')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    main(parse_args())

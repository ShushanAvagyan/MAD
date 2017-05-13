#!/usr/bin/env python

from argparse import ArgumentParser
import sys
from operator import itemgetter


DESCRIPTION = 'csvsort - sorts the rows of csv stream ascending.'
EXAMPLES = 'examples: cat stat.csv | csvsort -k shows'


def get_columns_indices(fields, all_columns):
    """Returns indices of specified columns"""
    indices = []
    for col_name in fields:
        if col_name.isdigit() and col_name not in all_columns:
            col_name = all_columns[int(col_name)]

        if '-' in col_name:
            start = col_name[:col_name.index('-')]
            end = col_name[col_name.index('-')+1:]
            if start.isdigit() and start not in all_columns:
                start = all_columns[int(start)]
            if end.isdigit() and end not in all_columns:
                end = all_columns[int(end)]
            if not start:
                for elem in range(all_columns.index(end)+1):
                    indices.append(elem)
            elif not end:
                for elem in range(all_columns.index(start), len(all_columns)):
                    indices.append(elem)
            else:
                for elem in range(all_columns.index(start),all_columns.index(end)+1):
                    indices.append(elem)
        else:
            indices.append(all_columns.index(col_name))

    return indices


def print_row(col_indices, row, output_stream):
    """Writes selected values from row to output_stream"""
    for i, index in enumerate(col_indices):
        output_stream.write(row[index])
        if i != len(col_indices) - 1:
            output_stream.write(',')
    output_stream.write('\n')


def main(args):
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'w') if args.output_file else sys.stdout
    all_columns = input_stream.readline().strip().split(args.separator)
    keys = args.keys.strip().split(',')
    keys = get_columns_indices(keys, all_columns)

    print_row(range(len(all_columns)), all_columns, output_stream)

    lines = []
    for i in range(args.max_rows):
        lines.append(input_stream.readline().strip().split(args.separator))
    lines = sorted(lines, key=itemgetter(*keys))
    for line in lines:
        print_row(range(len(line)),line,output_stream)
    if input_stream != sys.stdin:
        input_stream.close()
    if output_stream != sys.stdout:
        output_stream.close()


def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-s', '--separator', type=str, help='Separator to be used,\
                        Empty string used by default', default='')
    parser.add_argument('-o', '--output_file', type=str, help='Output file. \
                        Stdout is used by default')
    parser.add_argument('-k', '--keys', type=str, help="Specify list of keys\
                        (comma separated) to sort. Field names or field numbers \
                        can be used. Dash can be used to specify fields ranges.\
                        Range 'F1-F2' stands for all fields between F1 and F2. \
                        Range 'F1-' stands for all fields from F1 til the end.")
    parser.add_argument('--descending', help='If provided, perform descending \
                        sort instead of ascending', action='store_true')
    parser.add_argument('-m', '--max_rows', type=int, help="Don't load to memory more than \
                        MAX_ROWS rows at a time. This option is crucial if you \
                        have to deal with huge csv files. Default value is 0 that \
                        means that this will sort file in memory.",default=0)

    parser.add_argument('file', nargs='?', help='File to read input from.')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    main(parse_args())

#!/usr/bin/env python

from argparse import ArgumentParser
import sys


DESCRIPTION = 'csvcut - selects some columns from csv streem. Could change order of fields.'
EXAMPLES = 'example: csvcut -f 1,2 stat.txt csvcut -f st,shows,clicks stat.txt \
            cat stat.txt | csvcut -f shows,uniq,clicks \
            cat stat.txt | csvcut -f select_type-clicks all fields from select_type to clicks \
            cat stats.txt | csvcut -f -shows stat.txt all fields from the first till shows \
            csvcut -f page_id- all fields from page_id till the end \
            csvcut -f description --complement all fields except for description'


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
    fields = args.fields.strip().split(',')
    if args.unique:
        unique_fields = []
        for elem in fields:
            if elem not in unique_fields:
                unique_fields.append(elem)
        fields = unique_fields
    col_indices = get_columns_indices(fields, all_columns)
    if args.complement:
        col_indices = [i for i in range(len(all_columns)) if i not in col_indices]

    print_row(col_indices, all_columns, output_stream)
    for line in input_stream:
        row = line.strip().split(args.separator)
        print_row(col_indices, row, output_stream)

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
    parser.add_argument('-f', '--fields', type=str, help="Specify list of fields\
                        (comma separated) to cut. Field names or field numbers \
                        can be used. Dash can be used to specify fields ranges.\
                        Range 'F1-F2' stands for all fields between F1 and F2. \
                        Range 'F1-' stands for all fields from F1 til the end.")
    parser.add_argument('-c', '--complement', help='Instead of leaving only \
                        specified columns, leave all except specified', action='store_true')
    parser.add_argument('-u', '--unique', help='Remove duplicates from list of fields',
                        action='store_true')

    parser.add_argument('file', nargs='?', help='File to read input from.')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    main(parse_args())

from argparse import ArgumentParser
import sys

DESCRIPTION = 'csvhead'
EXAMPLES = 'csvhead -n -100 print first 100 rows.'

def main():
    args = parse_args()
    input_stream = open(args.file, 'r') if args.file else sys.stdin
    output_stream = open(args.output_file, 'w') if args.output_file else sys.stdout
    for line in range(args.lines_number+1):
        output_stream.write(input_stream.readline())
    if input_stream != sys.stdin:
        input_stream.close()
    if output_stream != sys.stdout:
        output_stream.close()

def parse_args():
    parser = ArgumentParser(description=DESCRIPTION, epilog=EXAMPLES)
    parser.add_argument('-n', '--lines_number', type=int, help='Number of lines used to set column width',
                        default=100)
    parser.add_argument('-o', '--output_file', type=str, help='Output file. stdout is used by default')
    parser.add_argument('file', nargs='?', help='File to read input from. stdin is used by default')
    args = parser.parse_args()
    return args

main()

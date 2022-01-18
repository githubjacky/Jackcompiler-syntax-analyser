from tokenize import TOKENIZER
from parse import PARSER
import sys


def main():
    jackFile = sys.argv[1]
    tokenize_file = TOKENIZER(f'{jackFile}')
    tokenize_file.tokenize_begin()
    tokenize_file.tokenize_end()
    # parse_file = PARSER(f'{tokenize_file.output}')
    # parse_file.parse_begin()
    # parse_file.parse_end()


if __name__ == '__main__':
    main()

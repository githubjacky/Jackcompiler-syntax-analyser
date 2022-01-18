from tokenize import TOKENIZER
from parse import PARSER
from text_compare import COMPARER
import sys


def main():
    jackFile = sys.argv[1]
    print('start to tokenize...')
    tokenize_file = TOKENIZER(f'{jackFile}')
    tokenize_file.tokenize_begin()
    tokenize_file.tokenize_end()
    print('start to parse...')
    parse_file = PARSER(tokenize_file.output)
    parse_file.parse_begin()
    parse_file.parse_end()

    response = input('do you want to check the result?(Yes:1/No:0)\n>> ')
    if int(response) == 1:
        print('start to compare...')
        comparer = COMPARER(parse_file.output)
        comparer.compare()
    else:
        print('analyze process has finished!')


if __name__ == '__main__':
    main()

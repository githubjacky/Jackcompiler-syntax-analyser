from tokenizer import TOKENIZER
from parser import PARSER

def main():
    # tokenize_file = TOKENIZER('../Square/SquareGame.jack')
    # tokenize_file.tokenize_begin()
    # tokenize_file.tokenize_end()
    parse_file = PARSER('test.xml')
    parse_file.parse_begin()
    parse_file.parse_end()

if __name__ == '__main__':
    main()
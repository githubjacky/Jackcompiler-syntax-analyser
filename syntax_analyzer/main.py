from tokenizer import TOKENIZER
# from parser import PARSER

def main():
    compile_file = TOKENIZER('../Square/SquareGame.jack')
    compile_file.tokenize_begin()
    compile_file.tokenize_end()

if __name__ == '__main__':
    main()
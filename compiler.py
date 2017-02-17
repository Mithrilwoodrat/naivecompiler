# -*- coding: utf-8 -*-


def ast_gen(text):
    parser = Parser()
    ast = parser.parse(data)
    return ast


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        source = f.read()
    ast = ast_gen(source)
    

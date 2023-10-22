import argparse

from latex_parser import LatexParser

lp = LatexParser()

if __name__ == '__main__':
    #parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("--string", type=str, help="string or path to file to parse")
    parser.add_argument("--from-file", type=str, help="boolean showing if --string it's a file or a literal string")

    args = parser.parse_args()
    string = args.string
    from_file = eval(args.from_file.capitalize())

    if from_file:
        with open(string, 'r') as f:
            s = f.read()
        
        print(lp.parse(s))
    
    else:
        print(lp.parse(string))



import argparse

parser = argparse.ArgumentParser(description="A test program")
parser.add_argument("add", nargs = "*", metavar="num", type=int, help="All the number separated by spaces will be aded")

args = parser.parse_args()

if len(args.add) != 0:
    print(sum(args.add))
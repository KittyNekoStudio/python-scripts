import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-o", "--output", help = "show output")
args = parser.parse_args()

if args.output:
    print("Hi")

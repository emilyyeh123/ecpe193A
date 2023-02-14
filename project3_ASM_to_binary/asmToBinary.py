'''
Program to convert MIPS Assembly to Machine Language
'''

import argparse

def main():
    finalStr = ""

    parser = argparse.ArgumentParser(description = "MIPs Assembly to Binary Converter")
    parser.add_argument("--input", required = True, help = "name of input file")
    parser.add_argument("--output", required = True, help = "name of output file")
    args = parser.parse_args()

    fileIn = open(args.input, "r")
    for line in fileIn:
        for instrElem in line.split():
            # perform conversion on current instruction
    fileIn.close()

    fileOut = open(args.output, "w")
    fileOut.write(finalStr)
    fileOut.close()

if __name__ == "__main__":
    main()

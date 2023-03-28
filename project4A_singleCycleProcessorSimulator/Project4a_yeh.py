'''
Python MIPS simulator that executes a subset of MIPS machine instructions

Run the file using:
python3 Project4a_yeh.py alpha.bin
'''
import sys

def main():
    f = sys.argv[1]

    fileIn = open(f, "r")
    
    for line in fileIn:
        line = line.split()
        print(line)

    fileIn.close()

if __name__ == "__main__":
    main()

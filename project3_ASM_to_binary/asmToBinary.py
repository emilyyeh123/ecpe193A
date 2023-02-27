'''
Program to convert MIPS Assembly to Machine Language

USE THE FOLLOWING COMMAND TO RUN THE PROGRAM:
python3 asmToBinary.py --file program1.asm

-----INSTRUCTIONS-----
R-Type:
    - FORMAT: 6 op, 5 rs, 5 rt, 5 rd, 5 shamt, 6 funct
    - All r-type op codes: 000000
    - add 
    - sub 
    - sll 
    - srl 
I-Type:
    - FORMAT: 6 op, 5 rs, 5 rt, 16 address/immediate
    - addi 001000
    - beq 000100
    - bne 000101
    - lw 100011
    - sw 101011
'''

import argparse

def main():
    finalStr = ""

    parser = argparse.ArgumentParser(description = "MIPs Assembly to Binary Converter")
    parser.add_argument("--file", required = True, help = "name of input file")
    #parser.add_argument("--output", required = True, help = "name of output file")
    args = parser.parse_args()

    fileIn = open(args.file, "r")
    for line in fileIn:
        for instrElem in line.split():
            for instr in instrElem.split(","):
                if instr == "add" or instr == "sub" or instr == "sll" or instr == "srl":
                        finalStr += "000000"
                elif instr == "addi":
                        finalStr += "001000"
                elif instr == "beq":
                        finalStr += "000100"
                elif instr == "bne":
                        finalStr += "000101"
                elif instr == "lw":
                        finalStr += "100011"
                elif instr == "sw":
                        finalStr += "101011"
                # perform conversion on current instruction
                print(instr)
        print("")
        finalStr += "\n"
    fileIn.close()

    #fileOut = open(args.output, "w")
    fileOut = open("out_code.txt", "w")
    fileOut.write(finalStr)
    fileOut.close()

if __name__ == "__main__":
    main()

'''
Program to convert MIPS Assembly to Machine Language

USE THE FOLLOWING COMMAND TO RUN THE PROGRAM:
python3 asmToBinary.py --file program1.asm

-----INSTRUCTIONS-----
R-Type:
    - FORMAT: 6 op, 5 rs, 5 rt, 5 rd, 5 shamt, 6 funct
    - All r-type op codes: 000000
    - add rd, rs, rt 100000 
    - sub rd, rs, rt 100010
    - sll rd, rt, sa 000000
    - srl rd, rt, sa 000010
    - slt rd, rs, rt 101010
I-Type:
    - FORMAT: 6 op, 5 rs, 5 rt, 16 address/immediate
    - addi rt, rs, imm 001000
    - beq rs, rt, label 000100
    - bne rs, rt, label 000101
    - lw rt, imm(rs) 100011
    - sw rt, imm(rs) 101011
'''

import argparse
import re

instrDict = {
    "r-type": ["add", "sub", "sll", "srl", "slt"],
    "i-type": ["addi", "beq", "bne", "lw", "sw"]
}

# initialize register dictionary
regDict = {
    "$zero": f'{0:05b}', # reg zero

    "$v0": f'{2:05b}', # reg v0, v1
    "$v1": f'{3:05b}',

    "$a0": f'{4:05b}', # reg a0-a3
    "$a1": f'{5:05b}',
    "$a2": f'{6:05b}',
    "$a3": f'{7:05b}',

    "$t0": f'{8:05b}', # reg t0-t7
    "$t1": f'{9:05b}',
    "$t2": f'{10:05b}',
    "$t3": f'{11:05b}',
    "$t4": f'{12:05b}',
    "$t5": f'{13:05b}',
    "$t6": f'{14:05b}',
    "$t7": f'{15:05b}',

    "$s0": f'{16:05b}', # reg s0-s7
    "$s1": f'{17:05b}',
    "$s2": f'{18:05b}',
    "$s3": f'{19:05b}',
    "$s4": f'{20:05b}',
    "$s5": f'{21:05b}',
    "$s6": f'{22:05b}',
    "$s7": f'{23:05b}',

    "$t8": f'{24:05b}', # reg t8, t9
    "$t9": f'{25:05b}',

    "$gp": f'{28:05b}',
    "$sp": f'{29:05b}',
    "$fp": f'{30:05b}',
    "$ra": f'{31:05b}'
}

def instrType(instr):
    for key, val in instrDict.items():
        if instr in val:
            return key
    return -1

# convert registers to binary
def regToBin(reg):
    # return 5-bit bin val of reg, -1 if reg not valid
    if reg in regDict.keys():
        return regDict.get(reg)

    try:
        reg = int(reg[1:]) # remove $ from str to get int
        if reg>=0 and reg<=31:
            return format(reg, "05b")
    except:
        pass

    return -1

# convert imm/shamt vals to binary
# if imm, bits parameter should be 16
# if shamt, bits parameter should be 5
# neg nums are converted to twos complement
def intToBin(bits, num):
    try:
        num = int(num)
        
        if num.bit_length() <= bits: #check if num fits within available bit length
            bitFormat = "0" + str(bits) + "b"

            if num < 0: # if neg num
                num = num * (-1)
                binNum = format(num, bitFormat)
                # flip bits
                binNum = binNum.replace("0", "2")
                binNum = binNum.replace("1", "0")
                binNum = binNum.replace("2", "1")
                # add 1
                binNum = format( int(binNum, 2) + int("1", 2) , bitFormat)
            else:
                binNum = format(num, bitFormat)
            return binNum
    except:
        pass

    return -1

def rTypeInstr(instrVals):
    # FORMAT: 6 op, 5 rs, 5 rt, 5 rd, 5 shamt, 6 funct
    # All r-type op codes: 000000
    op = format(0, "06b")
    rs = format(0, "05b")
    rt = format(0, "05b")
    rd = format(0, "05b")
    shamt = format(0, "05b")
    funct = format(0, "06b")
    lineBin = ""

    # add rd, rs, rt 100000 
    # sub rd, rs, rt 100010
    # slt rd, rs, rt 101010
    if instrVals[0] == "add" or instrVals[0] == "sub" or instrVals[0] == "slt":
        if len(instrVals) == 4: # check for proper amount of instructions
            if instrVals[0] == "add": 
                funct = "100000"
            elif instrVals[0] == "sub": 
                funct = "100010"
            elif instrVals[0] == "slt": 
                funct = "101010"
            rd = regToBin(instrVals[1])
            rs = regToBin(instrVals[2])
            rt = regToBin(instrVals[3])
            lineBin = op + rs + rt + rd + shamt + funct
            return lineBin
    
    # sll rd, rt, sa 000000
    # srl rd, rt, sa 000010
    elif instrVals[0] == "sll" or instrVals[0] == "srl":
        if len(instrVals) == 4: # check for proper amount of instructions
            if instrVals[0] == "sll": 
                funct = "000000"
            elif instrVals[0] == "srl": 
                funct = "000010"
            rd = regToBin(instrVals[1])
            rt = regToBin(instrVals[2])
            shamt = intToBin(5, instrVals[3])
            lineBin = op + rs + rt + rd + shamt + funct
            return lineBin

    return -1

def iTypeInstr(instrVals):
    # FORMAT: 6 op, 5 rs, 5 rt, 16 address/immediate
    op = format(0, "06b")
    rs = format(0, "05b")
    rt = format(0, "05b")
    imm = format(0, "016b")
    lineBin = ""

    # addi rt, rs, imm 001000
    if instrVals[0] == "addi":
        if len(instrVals) == 4: # check for proper amount of instructions
            op = "001000"
            rt = regToBin(instrVals[1])
            rs = regToBin(instrVals[2])
            imm = intToBin(16, instrVals[3])

    # beq rs, rt, label 000100
    # bne rs, rt, label 000101
    elif instrVals[0] == "beq" or instrVals[0] == "bne":
        if len(instrVals) == 4: # check for proper amount of instructions
            if instrVals[0] == "beq": 
                op = "000100"
            elif instrVals[0] == "bne": 
                op = "000101"
            instrVals[3] = int(instrVals[3])/4
            rs = regToBin(instrVals[1])
            rt = regToBin(instrVals[2])
            imm = intToBin(16, instrVals[3])

    # lw rt, imm(rs) 100011
    # sw rt, imm(rs) 101011
    elif instrVals[0] == "lw" or instrVals[0] == "sw":
        if len(instrVals) == 3: # check for proper amount of instructions
            if instrVals[0] == "lw": 
                op = "100011"
            elif instrVals[0] == "sw": 
                op = "101011"
            rt = regToBin(instrVals[1])
            immRS = instrVals[2].split("(") # separate instructions in second value
            imm = intToBin(16, immRS[0])
            rs = regToBin(immRS[1][:-1])

    if rs != -1 and rt != -1 and imm != -1:
            lineBin = op + rs + rt + imm
            return lineBin

    return -1

def main():
    finalStr = ""
    lineBin = ""
    inval = 0 # flag to check if input is invalid
    currType = -1

    parser = argparse.ArgumentParser(description = "MIPs Assembly to Binary Converter")
    parser.add_argument("--file", required = True, help = "name of input file")
    args = parser.parse_args()

    fileIn = open(args.file, "r")

    for line in fileIn:
        line = line.split("#", 1)[0]
        line = line.strip() # remove leading and trailing whitespace (including \n)

        if line != "": # if line not empty (if line not a comment)
            splitInstr = re.split("\\s+|,", line)
            #print(splitInstr, " ")

            currType = instrType(splitInstr[0])
            if currType == "r-type":
                lineBin = rTypeInstr(splitInstr)
            elif currType == "i-type":
                lineBin = iTypeInstr(splitInstr)
            else:
                inval = 1
                break

            if lineBin == -1:
                inval = 1
                break
            else:
                finalStr += lineBin

        finalStr += "\n"
    
    fileIn.close()

    # append invalid statement to output
    if inval == 1:
        finalStr += "!!! Invalid Input !!!\n"

    # write to output file
    fileOut = open("out_code.txt", "w")
    fileOut.write(finalStr)
    fileOut.close()

if __name__ == "__main__":
    main()

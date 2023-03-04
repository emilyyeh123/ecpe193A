'''
Program to convert MIPS Assembly to Machine Language

USE THE FOLLOWING COMMAND TO RUN THE PROGRAM:
python3 asmToBinary.py --file program1.asm

-----INSTRUCTIONS-----
R-Type:
    - FORMAT: 6 op, 5 rs, 5 rt, 5 rd, 5 shamt, 6 funct
    - All r-type op codes: 000000
    - add 100000 
    - sub 100010
    - sll 000000
    - srl 000010
    - slt 101010
I-Type:
    - FORMAT: 6 op, 5 rs, 5 rt, 16 address/immediate
    - addi 001000
    - beq 000100
    - bne 000101
    - lw 100011
    - sw 101011
'''

import argparse

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
    return 0 

def getRegBin(reg):
    # return 5-bit bin val of reg, 0 if reg not valid
    if reg in regDict.keys():
        return regDict.get(reg)

    try:
        reg = int(reg.replace("$", "")) # remove $ from str to get int
        if reg>=0 and reg<=31:
            return format(reg, "05b")
    except:
        return -1

def rTypeInstr(firstInstr, regs):
    # FORMAT: 6 op, 5 rs, 5 rt, 5 rd, 5 shamt, 6 funct
    strBin = ""
    rd = "00000"
    rs = "00000"
    rt = "00000"
    shamt = "00000"

    # All r-type op codes: 000000
    strBin += "000000"

    if len(regs) != 3:
        return 0

    if firstInstr == "add" or firstInstr == "sub" or firstInstr == "slt":
    # add rd, rs, rt 100000 
    # sub rd, rs, rt 100010
    # slt rd, rs, rt 101010

        for i in range(len(regs)):
        # get rs, rt, and rd vals
            thisReg = getRegBin(regs[i])
            if thisReg == -1:
                return 0
            elif i == 0:
                rd = thisReg
            elif i == 1:
                rs = thisReg
            elif i == 2:
                rt = thisReg

    elif firstInstr == "sll" or firstInstr == "srl":
    # sll rd, rt, shamt 000000
    # srl rd, rt, shamt 000010

        for i in range(len(regs)):
        # get rs, rt, and rd vals
            thisReg = getRegBin(regs[i])
            if thisReg == -1:
                return 0
            elif i == 0:
                rd = thisReg
            elif i == 1:
                rt = thisReg
            elif i == 2:
                shamt = thisReg

    # append rs, rt, rd, and shamt vals to binary str (in correct order)
    strBin += (rs + rt + rd + shamt)

    if firstInstr == "add":
        strBin += "100000"
    elif firstInstr == "sub":
        strBin += "100010"
    elif firstInstr == "slt":
        strBin += "101010"
    elif firstInstr == "sll":
        strBin += "000000"
    elif firstInstr == "srl":
        strBin += "000010"

    return strBin

def iTypeInstr(firstInstr, regs):
    # FORMAT: 6 op, 5 rs, 5 rt, 16 address/immediate
    # beq rs, rt, label 000100
    # bne rs, rt, label 000101
    # lw rt, imm(rs) 100011
    # sw rt, imm(rs) 101011
    strBin = ""
    rs = "00000"
    rt = "00000"
    imm = format(0, "016b")

    if firstInstr == "addi":
    # addi rt, rs, imm 001000

    return strBin

def main():
    finalStr = ""
    lineBin = ""
    inval = 0 # flag to check if input is invalid
    currType = 0

    parser = argparse.ArgumentParser(description = "MIPs Assembly to Binary Converter")
    parser.add_argument("--file", required = True, help = "name of input file")
    args = parser.parse_args()

    fileIn = open(args.file, "r")
    for line in fileIn:
        getInstr = line.split()
        if len(getInstr) != 2:
            inval = 1
            break

        firstInstr = getInstr[0]

        currType = instrType(firstInstr)
        if currType == 0:
            inval = 1
            break

        getInstr = getInstr[1].split(",")
        print(getInstr)
        if currType == "r-type":
            lineBin = rTypeInstr(firstInstr, getInstr)
        elif currType == "i-type":
            lineBin = iTypeInstr(firstInstr, getInstr)
        
        if lineBin == 0:
            inval = 1
            break
        else:
            finalStr += lineBin

        print("")
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

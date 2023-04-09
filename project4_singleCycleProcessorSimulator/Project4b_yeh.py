'''
Python MIPS simulator that executes a subset of MIPS machine instructions
Valid Instructions for part A: add, sub, addi
Valid Instructions for part B: add, sub, addi, beq, bne, lw, sw

Run PART B using:
python3 Project4b_yeh.py test0.bin memory.txt

out_control.txt:
- 10 bits specifying control signals for each clock cycle
- order of control signals: RegDst  ALUSrc  MemtoReg  RegWrite  MemRead  MemWrite  Branch  ALUOp1  ALUOp2  ZEROBIT

out_registers.txt:
- PC value in decimal followed by decimal values of first seven registers for each clk cycle
- format: <pc val>|<reg 0 val>|<reg 1 val>,..<reg 7 val>\n

out_memory.txt:
- final contents of memory, one word per line
'''

import sys

def writeCurrentPCReg(pcVal, regVals):
    pcRegStr = str(pcVal)
    for i in regVals:
        pcRegStr += "|" + str(i)
    return pcRegStr

def main():
    binInstr = []
    memVals = []

    controlSignal = ""
    pcRegVals = ""
    pcInit = 65536
    pc = pcInit # set curr pc val
    registers = [0,0,0,0,0,0,0,0]
    rs = rt = rd = -1
    imm = None
    lineNum = 0
    segFault = False

    # open bin file and store each line in a list
    inpFileName = sys.argv[1]
    binFile = open(inpFileName, "r")
    for line in binFile:
        binInstr.append(line.strip())
    binFile.close()

    # open memory file and store each line in a list
    inpFileName = sys.argv[2]
    memFile = open(inpFileName, "r")
    for line in memFile:
        try:
            memVals.append(int(line.strip()))
        except:
            pass
    memFile.close()

    # get max pc val
    numOfInstructions = len(binInstr)
    pcMax = pcInit + numOfInstructions*4

    # initialize first line of pc and register values
    pcRegVals += writeCurrentPCReg(pcInit, registers) + "\n"

    # seg fault if pc out of bounds or if memory out of bounds
    while not segFault:
        pc += 4

        # extract instruction opcode, rs, and rt
        instrOp = binInstr[lineNum][0:6]
        rs = int( binInstr[lineNum][6:11] , 2 ) # typecast binary reg val to dec
        rt = int( binInstr[lineNum][11:16] , 2 ) # typecast binary reg val to dec
        #print(pc, " | ", lineNum, "\t\t", instrOp, rs, rt)

        # Check if r-type instr
        if instrOp == "000000":
            # set control signal
            controlSignal += "100100010"

            # extract instruction func code & rd
            instrFunc = binInstr[lineNum][26:32]
            rd = int( binInstr[lineNum][16:21] , 2 ) # typecast binary reg val to dec

            if instrFunc == "100000":
                print("add   rd ", rd, " rs ", rs, " rt ", rt)
                # perform instruction on appropriate registers
                registers[rd] = registers[rs] + registers[rt]
            elif instrFunc == "100010":
                print("sub   rd ", rd, " rs ", rs, " rt ", rt)
                # perform instruction on appropriate registers
                registers[rd] = registers[rs] - registers[rt]

        # Check if i-type instr (assuming only addi instr is valid)
        elif instrOp == "001000":
            # set control signal
            controlSignal += "010100000"

            # extract instruction imm val
            # imm is twos comp
            # if first bit is 0, convert to dec normally
            # otherwise flip bits and add 1
            binNum = binInstr[lineNum][16:32]
            if binNum[0] == "0":
                imm = int( binNum , 2 )
            elif binNum[0] == "1":
                # flip bits
                binNum = binNum.replace("0", "2")
                binNum = binNum.replace("1", "0")
                binNum = binNum.replace("2", "1")
                # add 1 and set imm val
                imm = (int(binNum,2) + 1) * -1 
            print("addi  rt ", rt, " rs ", rs, " imm ", imm)

            # perform addi instr on appropriate registers
            registers[rt] = registers[rs] + imm

        controlSignal += "\n"
        pcRegVals += writeCurrentPCReg(pc, registers) + "\n"

        if lineNum == numOfInstructions-1 and pc == pcMax:
            break
        elif pc < pcInit or  pc > pcMax or lineNum >= 100:
            segFault = True
            break
        lineNum += 1

    if segFault == True:
        controlSignal += "!!! Segmentation Fault !!!\r\n"
        pcRegVals += "!!! Segmentation Fault !!!\r\n"

    # create and fill output files
    fileControlOut = open("out_control.txt", "w")
    fileRegOut = open("out_registers.txt", "w")

    fileControlOut.write(controlSignal)
    fileRegOut.write(pcRegVals)

    fileControlOut.close()
    fileRegOut.close()

if __name__ == "__main__":
    main()

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
        pc += 4 # increment pc for current instr

        # extract instruction opcode, rs, and rt
        instrOp = binInstr[lineNum][0:6]
        rs = int( binInstr[lineNum][6:11] , 2 ) # typecast binary reg val to dec
        rt = int( binInstr[lineNum][11:16] , 2 ) # typecast binary reg val to dec

        # Check if r-type instr
        if instrOp == "000000":
            # set control signal
            controlSignal += "1001000100"

            # extract instruction func code & rd
            instrFunc = binInstr[lineNum][26:32]
            rd = int( binInstr[lineNum][16:21] , 2 ) # typecast binary reg val to dec

            if instrFunc == "100000":
                # perform instruction on appropriate registers
                registers[rd] = registers[rs] + registers[rt]
            elif instrFunc == "100010":
                # perform instruction on appropriate registers
                registers[rd] = registers[rs] - registers[rt]
            
            if registers[rd] == 0:
                # set ALU zero bit high
                controlSignal = controlSignal[:-1] + "1"

        # otherwise, must be i-type instr
        else:
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

            # check if addi instr
            if instrOp == "001000":
                # set control signal
                controlSignal += "0101000000"
                # perform addi instr on appropriate registers
                registers[rt] = registers[rs] + imm

                if registers[rt] == 0:
                    # set ALU zero bit high
                    controlSignal = controlSignal[:-1] + "1"


            # check if beq instr
            elif instrOp == "000100":
                # set control signal
                controlSignal += "X0X0001010"
                # perform instr, update pc & lineNum as necessary 
                if registers[rt] == registers[rs]:
                    lineNum += imm
                    pc += (imm*4)

                if registers[rt] - registers[rs] == 0:
                    # set ALU zero bit high
                    controlSignal = controlSignal[:-1] + "1"

            # check if bne instr
            elif instrOp == "000101":
                # set control signal
                controlSignal += "X0X0001110"
                # perform instr, update pc & lineNum as necessary 
                if registers[rt] != registers[rs]:
                    lineNum += imm
                    pc += (imm*4)

                if registers[rt] - registers[rs] == 0:
                    # set ALU zero bit high
                    controlSignal = controlSignal[:-1] + "1"

            # check if lw instr
            elif instrOp == "100011":
                # set control signal
                controlSignal += "0111100000"
                # perform instr, get memory address, update register
                memAddress = int( (registers[rs] + imm)/4 ) # must segfault if invalid int
                registers[rt] = memVals[memAddress]

                if memAddress == 0:
                    # set ALU zero bit high
                    controlSignal = controlSignal[:-1] + "1"

            # check if sw instr
            elif instrOp == "101011":
                # set control signal
                controlSignal += "X1X0010000"
                # perform instr, get memory address, update val in memory
                memAddress = int( (registers[rs] + imm)/4 ) # must segfault if invalid int
                memVals[memAddress] = registers[rt]

                if memAddress == 0:
                    # set ALU zero bit high
                    controlSignal = controlSignal[:-1] + "1"

        controlSignal += "\n"
        pcRegVals += writeCurrentPCReg(pc, registers) + "\n"

        if lineNum == numOfInstructions-1 and pc == pcMax:
            # exit loop cleanly if end of file achieved
            break
        elif pc < pcInit or  pc > pcMax or lineNum >= 100:
            # set seg fault flag
            segFault = True
            break
        lineNum += 1 # increment line number for next instr

    if segFault == True:
        controlSignal += "!!! Segmentation Fault !!!\r\n"
        pcRegVals += "!!! Segmentation Fault !!!\r\n"

    # create and fill output files
    fileControlOut = open("out_control.txt", "w")
    fileControlOut.write(controlSignal)
    fileControlOut.close()

    fileRegOut = open("out_registers.txt", "w")
    fileRegOut.write(pcRegVals)
    fileRegOut.close()

    memOutStr = ""
    for i in memVals:
        memOutStr += (str(i) + "\n")
    fileMemOut = open("out_memory.txt", "w")
    fileMemOut.write(memOutStr)
    fileMemOut.close()

if __name__ == "__main__":
    main()

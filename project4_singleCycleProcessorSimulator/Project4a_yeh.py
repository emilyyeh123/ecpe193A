'''
Python MIPS simulator that executes a subset of MIPS machine instructions
Valid Instructions for part A: add, sub, addi
Valid Instructions for part B: add, sub, addi, beq, bne, lw, sw

Run the file using:
python3 Project4a_yeh.py alpha.bin

out_control.txt:
- 10 bits specifying control signals for each clock cycle
- order of control signals: RegDst  ALUSrc  MemtoReg  RegWrite  MemRead  MemWrite  Branch  ALUOp1  ALUOp2  ZEROBIT

out_registers.txt:
- PC value in decimal followed by decimal values of first seven registers for each clk cycle
- format: <pc val>|<reg 0 val>|<reg 1 val>,..<reg 7 val>\n
'''
import sys

def writeCurrentPCReg(pcVal, regVals):
    pcRegStr = str(pcVal)
    for i in regVals:
        pcRegStr += "|" + str(i)
    return pcRegStr

def main():
    controlSignal = ""
    pcRegVals = ""
    pc = 65536
    registers = [0,0,0,0,0,0,0,0]
    rs = rt = rd = -1
    imm = None
    lineNum = 0

    # initialize pc and register values
    pcRegVals += writeCurrentPCReg(pc, registers) + "\n"

    # open input file
    f = sys.argv[1]
    fileIn = open(f, "r")
    
    for line in fileIn:
        # should the program determine that more than 100 lines have been written,
        # the program should close the files and exit gracefully (this is unlikely)
        if lineNum <= 100: 
            line = line.split()
            pc += 4

            # extract instruction opcode, rs, and rt
            instrOp = line[0][0:6]
            rs = int( line[0][6:11] , 2 ) # typecast binary reg val to dec
            rt = int( line[0][11:16] , 2 ) # typecast binary reg val to dec

            # Check if r-type instr
            if instrOp == "000000":
                # set control signal
                controlSignal += "1001000100"

                # extract instruction func code & rd
                instrFunc = line[0][26:32]
                rd = int( line[0][16:21] , 2 ) # typecast binary reg val to dec

                if instrFunc == "100000":
                    #print("add   rd ", rd, " rs ", rs, " rt ", rt)
                    # perform instruction on appropriate registers
                    registers[rd] = registers[rs] + registers[rt]
                elif instrFunc == "100010":
                    #print("sub   rd ", rd, " rs ", rs, " rt ", rt)
                    # perform instruction on appropriate registers
                    registers[rd] = registers[rs] - registers[rt]

            # Check if i-type instr (assuming only addi instr is valid)
            elif instrOp == "001000":
                # set control signal
                controlSignal += "0101000000"

                # extract instruction imm val
                # imm is twos comp
                # if first bit is 0, convert to dec normally
                # otherwise flip bits and add 1
                binNum = line[0][16:32]
                if binNum[0] == "0":
                    imm = int( binNum , 2 )
                elif binNum[0] == "1":
                    # flip bits
                    binNum = binNum.replace("0", "2")
                    binNum = binNum.replace("1", "0")
                    binNum = binNum.replace("2", "1")
                    # add 1 and set imm val
                    imm = (int(binNum,2) + 1) * -1 
                #print("addi  rt ", rt, " rs ", rs, " imm ", imm)

                # perform addi instr on appropriate registers
                registers[rt] = registers[rs] + imm

            controlSignal += "\n"
            pcRegVals += writeCurrentPCReg(pc, registers) + "\n"
            lineNum += 1

    fileIn.close()

    # create and fill output files
    fileControlOut = open("out_control.txt", "w")
    fileRegOut = open("out_registers.txt", "w")

    fileControlOut.write(controlSignal)
    fileRegOut.write(pcRegVals)

    fileControlOut.close()
    fileRegOut.close()

if __name__ == "__main__":
    main()

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

    # initialize pc and register values
    pcRegVals += writeCurrentPCReg(pc, registers) + "\n"

    # open input file
    f = sys.argv[1]
    fileIn = open(f, "r")
    
    for line in fileIn:
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
                print("add   rd ", rd, " rs ", rs, " rt ", rt)
            elif instrFunc == "100010":
                print("sub   rd ", rd, " rs ", rs, " rt ", rt)

        # Check if i-type instr
        elif instrOp == "001000":
            # set control signal
            controlSignal += "0101000000"

            # extract instruction func code & rd
            imm = int( line[0][16:32] , 2 )
            print("addi  rt ", rt, " rs ", rs, " imm ", imm)

        controlSignal += "\n"
        pcRegVals += writeCurrentPCReg(pc, registers) + "\n"

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

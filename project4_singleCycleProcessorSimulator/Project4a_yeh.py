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

def main():
    pc = 65536
    controlSignal = ""
    pcRegVals = str(pc) + "|0|0|0|0|0|0|0|0\n" # initial state of pc & regs

    # open input file
    f = sys.argv[1]
    fileIn = open(f, "r")
    
    for line in fileIn:
        line = line.split()
        pc += 4
        pcRegVals += str(pc) + "|"

        # extract instruction opcode
        instrOp = line[0][0:6]
        if instrOp == "000000":
            # r-type instr
            controlSignal += "1001000100"
            instrFunc = line[0][26:32]
            if instrFunc == "100000":
                print("add func")
            elif instrFunc == "100010":
                print("sub func")
        # if i-type instr, then ALUOPcode = 00
        elif instrOp == "001000":
            controlSignal += "0101000000"
            print("i-type instr")

        controlSignal += "\n"
        pcRegVals += "\n"

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

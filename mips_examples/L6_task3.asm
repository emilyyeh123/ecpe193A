# Task 3: Design a full program based off the following C code and test it in QtSPIM
# USE: bne, beq, slt
# DON'T USE PSEUDO INST. (ex: bge, blt, ble, etc.)

# int array[7];
# int main(){
#   int i = 0;
#   array[0] = 5;
#   for(i = 1; i < 7; i++)
#       array[i] = i + array[i-1];
# }

.globl main

main:
    # Register Map
    # t0 = i
    # s0 = array
    # t1 = constant 7
    # t2 = constant 5
    # t3 = binary value if i < 7

    add $t0, $zero, $zero # i = 0
    la $s0, arr # load base address

    addi $t2, $zero, 5 # const. val. 5
    sw $t2, 0($s0) # array[0] = 5

    addi $t1, $zero, 7 # constant 7
    addi $t0, $zero, 1 # i = 1

    for:
        slt $t3, $t0, $t1 # set t3 if i < 7
        beq $t3, $zero, outsidefor
        
        # load array[i-1]
        addi $t4, $t0, -1 # i-1
        add $t4, $t4, $t4
        add $t4, $t4, $t4 # 4*(i-1), offset address by 4
        add $t4, $s0, $t4 # t4 = base + proper offset => &arr[i-1]
        lw $t5, 0($t4) # t5 = array[i-1]

        # perform computation
        add $t5, $t0, $t5 # t5 = i + arr[i-]

        # store result at arr[i]
        addi $t4, $t0, 0 # this line unnecessary; i = 0
        add $t4, $t4, $t4
        add $t4, $t4, $t4 # 4*(i-1), offset address by 4
        add $t4, $s0, $t4 # t4 = base + proper offset => &arr[i-1]
        sw $t5, 0($t4) #store result at arr[i]

        addi $t0, $t0, 1 # i++
        j for

    outsidefor:

    # exit
    li $v0, 10
    syscall

.data
arr: .word 28 # array[7], 4 bytes per element


.globl main
.text

main:
    lw $s0, a #s0 is for a
    lw $s1, B #s1 is for b
    lw $s2, c #s2 is for c

    #use your own choice of t reg. for the variable i
    # your code here
    whileLoop:
    blt $s2, $zero, exitWhile # if c<0, exit
    addi $t0, $zero, $zero # initialize t0

    forLoop:
    addi $t0, $t0, 1 # i++
    addi $s1, $s1, 1 # b++
    bge $t0, $s0, whileLoop # if i >= a, exit

    j forLoop

    exitWhile:



    #exit program
    li $v0, 10
    syscall

.data
a: .word 4
B: .word 5
c: .word 6

# CONVERT THE FOLLOWING C CODE TO MIPS

# int main() {
# int arr[]={10, 9, 8, 7, 6, 5, 4, 3, 2, 1},n=10,i,j,temp;    
# for (i = 0; i < n - 1; i++)
#    for (j = 0; j < n - i - 1; j++)
#    {
#      if (arr[j] > arr[j + 1])
#      {
#         temp=arr[j];
#         arr[j]=arr[j+1];
#         arr[j+1]=temp;
#      }
#   }
# }

.globl main

main:

# REGISTER MAP:
# s0 = array
# s1 = n
# s5 = arr[j]
# s6 = arr[j+1]
# t0 = i
# t1 = j
# t2 = temp (address of arr[j])
# t3 = n-1
# t4 = n-i-1
# t5 = binary value for slt instruction

la $s0, arr # load array into s0
#lw $s1, n # initialize register s1 to value of var n
addi $s1, $zero, 10 # initialize register s1 to value of var n

add $t0, $zero, $zero # initialize i = 0
addi $t3, $s1, -1 # t3 = n-1
ifor: # begin contents of outer i loop
bge $t0, $t3, exitfor # if i >= n-1, exit loop

sub $t4, $t3, $t0 # t4 = n-1 - i = t3-i
addi $t0, $t0, 1 # i++
add $t1, $zero, $zero # initialize j = 0
add $t2, $s0, $zero # set temp (reset addr of j at first element of array)

jfor: # begin contents of inner j loop
#bge $t1, $t4, ifor  # if j >= n-i-1, exit inner j loop and return to outer i loop
slt $t5, $t1, $t4  # t5 = 0 if j<n-i-1 is FALSE 
beq $t5, $zero, ifor # if j<n-i-1 is FALSE, exit inner j loop and return to outer i loop

lw $s5, 0($t2) # arr[j]
lw $s6, 4($t2) # arr[j+1]

#ble $s5, $s6, noSwap # only swap if arr[j] > arr[j+1], otherwise noSwap
slt $t5, $s6, $s5 # t5 is true if arr[j+1] < arr[j]
beq $t5, $zero, noSwap # if arr[j+1] !< arr[j], DONT SWAP
sw $s5, 4($t2) # arr[j] = arr[j+1]
sw $s6, 0($t2) # arr[j+1] = temp

noSwap:

addi $t1, $t1, 1 # j++
add $t2, $t1, $t1 # t2 = j+j = 2j
add $t2, $t2, $t2 # t2 = 2j+2j = 4j
add $t2, $s0, $t2 # t2 = arr address + offset = &arr[j]
j jfor # loop back through inner j loop

exitfor:

# exit
li $v0, 10
syscall

.data
arr: .word 10, 9, 8, 7, 6, 5, 4, 3, 2, 1
#n: .word 10
#arr: .word 3, 5, 8, 6, 1, 1, 6, 3, 4, 1, 1, 5, 2, 1, 7
#n: .word 15

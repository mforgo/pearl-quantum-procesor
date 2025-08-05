# programs/myprogram.asm
# Sample program: compute 5 + 3, store result, compare, conditional jump

mov 5 p0         # Load immediate 5 into register p0
mov 3 p1         # Load immediate 3 into register p1

add p0 p1        # p0 = p0 + p1       ; 5+3=8
mov p0 h100      # Store result 8 at memory address 100

cmp p0 p1        # Compare p0 > p1     ; 8 > 3 → b = true
jmpif 8          # If true, jump to line 8

# If comparison was false, zero p2:
mov 0 p2         # p2 = 0
jmp 9            # Skip the next instruction

# If comparison was true, set p2 = 1:
mov 1 p2         # p2 = 1

# End of program

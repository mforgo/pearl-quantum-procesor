# io_demo.asm
# IN, OUT instructions demo

in p0             # read first number into p0
in p1             # read second number into p1

add p0 p1         # p0 ← p0 + p1
out p0            # OUT: sum

# Compare to constant 10
mov 10 p2         # p2 ← 10
cmp p0 p2         # b ← (sum > 10)?
jmpif 12          # if sum > 10, skip
out p2            # OUT: 10 (if sum ≤ 10)

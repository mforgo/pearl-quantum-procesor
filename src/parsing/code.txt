in p1
in p2
eqq p0 p1
jmpif 15
eqq p0 p2
jmpif 14
eqq p1 p2
jmpif 10
gt p2 p1
jmpif 12
sub p1 p2
jmp 13
sub p2 p1
jmp 6
mov p2 p1
out p1
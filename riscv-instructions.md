RARS supports all instruction in RV32imfd. Additionally it supports `uret` from extension n, and `wfi` from the privileged specification. rv64 mode instructions are not included here and instead have their own page [[Differences between 32 bit and 64 bit modes]]. Fence instructions do nothing as RARS doesn't have a cache.

If there is an instruction from RV32imfd missing, that's a bug. Additionally, all psuedo-instructions listed in the spec should also be supported. 

| Example Usage | Description |
|---------------|-------------|
|add t1,t2,t3|Addition: set t1 to (t2 plus t3)|
|addi t1,t2,-100|Addition immediate: set t1 to (t2 plus signed 12-bit immediate)|
|and t1,t2,t3|Bitwise AND : Set t1 to bitwise AND of t2 and t3|
|andi t1,t2,-100|Bitwise AND immediate : Set t1 to bitwise AND of t2 and sign-extended 12-bit immediate|
|auipc t1,100000|Add upper immediate to pc: set t1 to (pc plus an upper 20-bit immediate)|
|beq t1,t2,label|Branch if equal : Branch to statement at label's address if t1 and t2 are equal|
|bge t1,t2,label|Branch if greater than or equal: Branch to statement at label's address if t1 is greater than or equal to t2|
|bgeu t1,t2,label|Branch if greater than or equal to (unsigned): Branch to statement at label's address if t1 is greater than or equal to t2 (with an unsigned interpretation)|
|blt t1,t2,label|Branch if less than: Branch to statement at label's address if t1 is less than t2|
|bltu t1,t2,label|Branch if less than (unsigned): Branch to statement at label's address if t1 is less than t2 (with an unsigned interpretation)|
|bne t1,t2,label|Branch if not equal : Branch to statement at label's address if t1 and t2 are not equal|
|csrrc t0, fcsr, t1|Atomic Read/Clear CSR: read from the CSR into t0 and clear bits of the CSR according to t1|
|csrrci t0, fcsr, 10|Atomic Read/Clear CSR Immediate: read from the CSR into t0 and clear bits of the CSR according to a constant|
|csrrs t0, fcsr, t1|Atomic Read/Set CSR: read from the CSR into t0 and logical or t1 into the CSR|
|csrrsi t0, fcsr, 10|Atomic Read/Set CSR Immediate: read from the CSR into t0 and logical or a constant into the CSR|
|csrrw t0, fcsr, t1|Atomic Read/Write CSR: read from the CSR into t0 and write t1 into the CSR|
|csrrwi t0, fcsr, 10|Atomic Read/Write CSR Immediate: read from the CSR into t0 and write a constant into the CSR|
|div t1,t2,t3|Division: set t1 to the result of t2/t3|
|divu t1,t2,t3|Division: set t1 to the result of t2/t3 using unsigned division|
|ebreak|Pause execution|
|ecall|Issue a system call : Execute the system call specified by value in a7|
|fadd.d f1, f2, f3, dyn|Floating ADD (64 bit): assigns f1 to f2 + f3|
|fadd.s f1, f2, f3, dyn|Floating ADD: assigns f1 to f2 + f3|
|fclass.d t1, f1|Classify a floating point number (64 bit)|
|fclass.s t1, f1|Classify a floating point number|
|fcvt.d.s t1, f1, dyn|Convert a float to a double: Assigned the value of f2 to f1|
|fcvt.d.w f1, t1, dyn|Convert double from integer: Assigns the value of t1 to f1|
|fcvt.d.wu f1, t1, dyn|Convert double from unsigned integer: Assigns the value of t1 to f1|
|fcvt.s.d t1, f1, dyn|Convert a double to a float: Assigned the value of f2 to f1|
|fcvt.s.w f1, t1, dyn|Convert float from integer: Assigns the value of t1 to f1|
|fcvt.s.wu f1, t1, dyn|Convert float from unsigned integer: Assigns the value of t1 to f1|
|fcvt.w.d t1, f1, dyn|Convert integer from double: Assigns the value of f1 (rounded) to t1|
|fcvt.w.s t1, f1, dyn|Convert integer from float: Assigns the value of f1 (rounded) to t1|
|fcvt.wu.d t1, f1, dyn|Convert unsinged integer from double: Assigns the value of f1 (rounded) to t1|
|fcvt.wu.s t1, f1, dyn|Convert unsinged integer from float: Assigns the value of f1 (rounded) to t1|
|fdiv.d f1, f2, f3, dyn|Floating DIVide (64 bit): assigns f1 to f2 / f3|
|fdiv.s f1, f2, f3, dyn|Floating DIVide: assigns f1 to f2 / f3|
|fence 1, 1|Ensure that IO and memory accesses before the fence happen before the following IO and memory accesses as viewed by a different thread|
|fence.i|Ensure that stores to instruction memory are visible to instruction fetches|
|feq.d t1, f1, f2|Floating EQuals (64 bit): if f1 = f2, set t1 to 1, else set t1 to 0|
|feq.s t1, f1, f2|Floating EQuals: if f1 = f2, set t1 to 1, else set t1 to 0|
|fld f1, -100(t1)|Load a double from memory|
|fle.d t1, f1, f2|Floating Less than or Equals (64 bit): if f1 <= f2, set t1 to 1, else set t1 to 0|
|fle.s t1, f1, f2|Floating Less than or Equals: if f1 <= f2, set t1 to 1, else set t1 to 0|
|flt.d t1, f1, f2|Floating Less Than (64 bit): if f1 < f2, set t1 to 1, else set t1 to 0|
|flt.s t1, f1, f2|Floating Less Than: if f1 < f2, set t1 to 1, else set t1 to 0|
|flw f1, -100(t1)|Load a float from memory|
|fmadd.d f1, f2, f3, f4, dyn|Fused Multiply Add (64 bit): Assigns f2*f3+f4 to f1|
|fmadd.s f1, f2, f3, f4, dyn|Fused Multiply Add: Assigns f2*f3+f4 to f1|
|fmax.d f1, f2, f3|Floating MAXimum (64 bit): assigns f1 to the larger of f1 and f3|
|fmax.s f1, f2, f3|Floating MAXimum: assigns f1 to the larger of f1 and f3|
|fmin.d f1, f2, f3|Floating MINimum (64 bit): assigns f1 to the smaller of f1 and f3|
|fmin.s f1, f2, f3|Floating MINimum: assigns f1 to the smaller of f1 and f3|
|fmsub.d f1, f2, f3, f4, dyn|Fused Multiply Subatract: Assigns f2*f3-f4 to f1|
|fmsub.s f1, f2, f3, f4, dyn|Fused Multiply Subatract: Assigns f2*f3-f4 to f1|
|fmul.d f1, f2, f3, dyn|Floating MULtiply (64 bit): assigns f1 to f2 * f3|
|fmul.s f1, f2, f3, dyn|Floating MULtiply: assigns f1 to f2 * f3|
|fmv.s.x f1, t1|Move float: move bits representing a float from an integer register|
|fmv.x.s t1, f1|Move float: move bits representing a float to an integer register|
|fnmadd.d f1, f2, f3, f4, dyn|Fused Negate Multiply Add (64 bit): Assigns -(f2*f3+f4) to f1|
|fnmadd.s f1, f2, f3, f4, dyn|Fused Negate Multiply Add: Assigns -(f2*f3+f4) to f1|
|fnmsub.d f1, f2, f3, f4, dyn|Fused Negated Multiply Subatract: Assigns -(f2*f3-f4) to f1|
|fnmsub.s f1, f2, f3, f4, dyn|Fused Negated Multiply Subatract: Assigns -(f2*f3-f4) to f1|
|fsd f1, -100(t1)|Store a double to memory|
|fsgnj.d f1, f2, f3|Floating point sign injection (64 bit): replace the sign bit of f2 with the sign bit of f3 and assign it to f1|
|fsgnj.s f1, f2, f3|Floating point sign injection: replace the sign bit of f2 with the sign bit of f3 and assign it to f1|
|fsgnjn.d f1, f2, f3|Floating point sign injection (inverted 64 bit):  replace the sign bit of f2 with the opposite of sign bit of f3 and assign it to f1|
|fsgnjn.s f1, f2, f3|Floating point sign injection (inverted):  replace the sign bit of f2 with the opposite of sign bit of f3 and assign it to f1|
|fsgnjx.d f1, f2, f3|Floating point sign injection (xor 64 bit):  xor the sign bit of f2 with the sign bit of f3 and assign it to f1|
|fsgnjx.s f1, f2, f3|Floating point sign injection (xor):  xor the sign bit of f2 with the sign bit of f3 and assign it to f1|
|fsqrt.d f1, f2, dyn|Floating SQuare RooT (64 bit): Assigns f1 to the square root of f2|
|fsqrt.s f1, f2, dyn|Floating SQuare RooT: Assigns f1 to the square root of f2|
|fsub.d f1, f2, f3, dyn|Floating SUBtract (64 bit): assigns f1 to f2 - f3|
|fsub.s f1, f2, f3, dyn|Floating SUBtract: assigns f1 to f2 - f3|
|fsw f1, -100(t1)|Store a float to memory|
|jal t1, target|Jump and link : Set t1 to Program Counter (return address) then jump to statement at target address|
|jalr t1, t2, -100|Jump and link register: Set t1 to Program Counter (return address) then jump to statement at t2 + immediate|
|lb t1, -100(t2)|Set t1 to sign-extended 8-bit value from effective memory byte address|
|lbu t1, -100(t2)|Set t1 to zero-extended 8-bit value from effective memory byte address|
|lh t1, -100(t2)|Set t1 to sign-extended 16-bit value from effective memory halfword address|
|lhu t1, -100(t2)|Set t1 to zero-extended 16-bit value from effective memory halfword address|
|lui t1,100000|Load upper immediate: set t1 to 20-bit followed by 12 0s|
|lw t1, -100(t2)|Set t1 to contents of effective memory word address|
|mul t1,t2,t3|Multiplication: set t1 to the lower 32 bits of t2*t3|
|mulh t1,t2,t3|Multiplication: set t1 to the upper 32 bits of t2*t3 using signed multiplication|
|mulhsu t1,t2,t3|Multiplication: set t1 to the upper 32 bits of t2*t3 where t2 is signed and %t3 is unsigned|
|mulhu t1,t2,t3|Multiplication: set t1 to the upper 32 bits of t2*t3 using unsigned multiplication|
|or t1,t2,t3|Bitwise OR : Set t1 to bitwise OR of t2 and t3|
|ori t1,t2,-100|Bitwise OR immediate : Set t1 to bitwise OR of t2 and sign-extended 12-bit immediate|
|rem t1,t2,t3|Remainder: set t1 to the remainder of t2/t3|
|remu t1,t2,t3|Remainder: set t1 to the remainder of t2/t3 using unsigned division|
|sb t1, -100(t2)|Store byte : Store the low-order 8 bits of t1 into the effective memory byte address|
|sh t1, -100(t2)|Store halfword : Store the low-order 16 bits of t1 into the effective memory halfword address|
|sll t1,t2,t3|Shift left logical: Set t1 to result of shifting t2 left by number of bits specified by value in low-order 5 bits of t3|
|slli t1,t2,10|Shift left logical : Set t1 to result of shifting t2 left by number of bits specified by immediate|
|slt t1,t2,t3|Set less than : If t2 is less than t3, then set t1 to 1 else set t1 to 0|
|slti t1,t2,-100|Set less than immediate : If t2 is less than sign-extended 12-bit immediate, then set t1 to 1 else set t1 to 0|
|sltiu t1,t2,-100|Set less than immediate unsigned : If t2 is less than  sign-extended 16-bit immediate using unsigned comparison, then set t1 to 1 else set t1 to 0|
|sltu t1,t2,t3|Set less than : If t2 is less than t3 using unsigned comparision, then set t1 to 1 else set t1 to 0|
|sra t1,t2,t3|Shift right arithmetic: Set t1 to result of sign-extended shifting t2 right by number of bits specified by value in low-order 5 bits of t3|
|srai t1,t2,10|Shift right arithmetic : Set t1 to result of sign-extended shifting t2 right by number of bits specified by immediate|
|srl t1,t2,t3|Shift right logical: Set t1 to result of shifting t2 right by number of bits specified by value in low-order 5 bits of t3|
|srli t1,t2,10|Shift right logical : Set t1 to result of shifting t2 right by number of bits specified by immediate|
|sub t1,t2,t3|Subtraction: set t1 to (t2 minus t3)|
|sw t1, -100(t2)|Store word : Store contents of t1 into effective memory word address|
|uret|Return from handling an interrupt or exception (to uepc)|
|wfi|Wait for Interrupt|
|xor t1,t2,t3|Bitwise XOR : Set t1 to bitwise XOR of t2 and t3|
|xori t1,t2,-100|Bitwise XOR immediate : Set t1 to bitwise XOR of t2 and sign-extended 12-bit immediate|

Supported psuedo-instructions:

| Example Usage | Description |
|---------------|-------------|
|addi t1,t2,%lo(label) |Load Lower Address : Set t1 to t2 + lower 12-bit label's address|
|b label       |Branch : Branch to statement at label unconditionally|
|beqz t1,label |Branch if EQual Zero : Branch to statement at label if t1 == 0|
|bgez t1,label |Branch if Greater than or Equal to Zero : Branch to statement at label if t1 >= 0|
|bgt  t1,t2,label |Branch if Greater Than : Branch to statement at label if t1 > t2|
|bgtu t1,t2,label |Branch if Greater Than Unsigned: Branch to statement at label if t1 > t2 (unsigned compare)|
|bgtz t1,label |Branch if Greater Than: Branch to statement at label if t1 > 0|
|ble  t1,t2,label |Branch if Less or Equal : Branch to statement at label if t1 <= t2|
|bleu t1,t2,label |Branch if Less or Equal Unsigned : Branch to statement at label if t1 <= t2 (unsigned compare)|
|blez t1,label |Branch if Less than or Equal to Zero : Branch to statement at label if t1 <= 0|
|bltz t1,label |Branch if Less Than Zero : Branch to statement at label if t1 < 0|
|bnez t1,label |Branch if Not Equal Zero : Branch to statement at label if t1 != 0|
|call label     |CALL: call a far-away subroutine|
|csrc t1, fcsr |Clear bits in control and status register|
|csrci fcsr, 100 |Clear bits in control and status register|
|csrr t1, fcsr |Read control and status register|
|csrs t1, fcsr |Set bits in control and status register|
|csrsi fcsr, 100 |Set bits in control and status register|
|csrw t1, fcsr |Write control and status register|
|csrwi fcsr, 100 |Write control and status register|
|fabs.d f1, f2 | Set f1 to the absolute value of f2 (64 bit)|
|fabs.s f1, f2 | Set f1 to the absolute value of f2|
|fadd.d    f1, f2, f3     |Floating ADD (64 bit): assigns f1 to f2 + f3|
|fadd.s    f1, f2, f3     |Floating ADD: assigns f1 to f2 + f3|
|fcvt.d.s f1, f2          |Convert float to double: Assigned the value of f2 to f1|
|fcvt.d.w  f1, t1         |Convert double from signed integer: Assigns the value of t1 to f1|
|fcvt.d.wu f1, t1         |Convert double from unsigned integer: Assigns the value of t1 to f1|
|fcvt.s.d f1, f2          |Convert double to float: Assigned the value of f2 to f1|
|fcvt.s.w  f1, t1         |Convert float from signed integer: Assigns the value of t1 to f1|
|fcvt.s.wu f1, t1         |Convert float from unsigned integer: Assigns the value of t1 to f1|
|fcvt.w.d  t1, f1         |Convert signed integer from double: Assigns the value of f1 (rounded) to t1|
|fcvt.w.s  t1, f1         |Convert signed integer from float: Assigns the value of f1 (rounded) to t1|
|fcvt.wu.d t1, f1         |Convert unsigned integer from double: Assigns the value of f1 (rounded) to t1|
|fcvt.wu.s t1, f1         |Convert unsigned integer from float: Assigns the value of f1 (rounded) to t1|
|fdiv.d    f1, f2, f3     |Floating DIVide (64 bit): assigns f1 to f2 / f3|
|fdiv.s    f1, f2, f3     |Floating DIVide: assigns f1 to f2 / f3|
|fge.d t1, f2, f3      |Floating Greater Than or Equal (64 bit): if f1 >= f2, set t1 to 1, else set t1 to 0|
|fge.s t1, f2, f3      |Floating Greater Than or Equal: if f1 >= f2, set t1 to 1, else set t1 to 0|
|fgt.d t1, f2, f3      |Floating Greater Than (64 bit): if f1 > f2, set t1 to 1, else set t1 to 0|
|fgt.s t1, f2, f3      |Floating Greater Than: if f1 > f2, set t1 to 1, else set t1 to 0|
|fld f1,(t2)       |Load Word: Set f1 to 64-bit value from effective memory word address|
|fld f1,-100       |Load Word: Set f1 to 64-bit value from effective memory word address|
|fld f1,10000000,t3|Load Word: Set f1 to 64-bit value from effective memory word address using t3 as a temporary|
|fld f1,label, t3  |Load Word: Set f1 to 64-bit value from effective memory word address using t3 as a temporary|
|flw f1,%lo(label)(t2) |Load from Address|
|flw f1,(t2)     |Load Word Coprocessor 1 : Set f1 to 32-bit value from effective memory word address|
|flw f1,-100     |Load Word Coprocessor 1 : Set f1 to 32-bit value from effective memory word address|
|flw f1,10000000,t3|Load Word Coprocessor 1 : Set f1 to 32-bit value from effective memory word address using t3 as a temporary|
|flw f1,label, t3|Load Word Coprocessor 1 : Set f1 to 32-bit value from effective memory word address using t3 as a temporary|
|flwd f1,%lo(label)(t2) |Load from Address|
|fmadd.d   f1, f2, f3, f4 |Fused Multiply Add (64 bit): Assigns f2*f3+f4 to f1|
|fmadd.s   f1, f2, f3, f4 |Fused Multiply Add: Assigns f2*f3+f4 to f1|
|fmsub.d   f1, f2, f3, f4 |Fused Multiply Subatract (64 bit): Assigns f2*f3-f4 to f1|
|fmsub.s   f1, f2, f3, f4 |Fused Multiply Subatract: Assigns f2*f3-f4 to f1|
|fmul.d    f1, f2, f3     |Floating MULtiply (64 bit): assigns f1 to f2 * f3|
|fmul.s    f1, f2, f3     |Floating MULtiply: assigns f1 to f2 * f3|
|fmv.d  f1, f2 | Move the value of f2 to f1 (64 bit)|
|fmv.s  f1, f2 | Move the value of f2 to f1|
|fmv.w.x t1, f1 |Move float (New mnemonic): move bits representing a float from an integer register|
|fmv.x.w t1, f1 |Move float (New mnemonic): move bits representing a float to an integer register|
|fneg.d f1, f2 | Set f1 to the negation of f2 (64 bit)|
|fneg.s f1, f2 | Set f1 to the negation of f2|
|fnmadd.d  f1, f2, f3, f4 |Fused Negate Multiply Add (64 bit): Assigns -(f2*f3+f4) to f1|
|fnmadd.s  f1, f2, f3, f4 |Fused Negate Multiply Add: Assigns -(f2*f3+f4) to f1|
|fnmsub.d  f1, f2, f3, f4 |Fused Negated Multiply Subatract (64 bit): Assigns -(f2*f3-f4) to f1|
|fnmsub.s  f1, f2, f3, f4 |Fused Negated Multiply Subatract: Assigns -(f2*f3-f4) to f1|
|frcsr t1     |Read FP control/status register|
|frflags t1      |Read FP exception flags|
|frrm t1      |Read FP rounding mode|
|frsr t1     |Alias for frcsr t1|
|fscsr t1     |Write FP control/status register|
|fscsr t1, t2 |Swap FP control/status register|
|fsd f1,(t2)       |Store Word: Store 64-bit value from f1 to effective memory word address|
|fsd f1,-100       |Store Word: Store 64-bit value from f1 to effective memory word address|
|fsd f1,10000000,t3|Store Word: Store 64-bit value from f1 to effective memory word address using t3 as a temporary|
|fsd f1,label, t3  |Store Word: Store 64-bit value from f1 to effective memory word address using t3 as a temporary|
|fsflags t1      |Write FP exception flags|
|fsflags t1, t2  |Swap FP exception flags|
|fsflagsi 100     |Write FP exception flags, immediate|
|fsflagsi t1, 100 |Swap FP exception flags, immediate|
|fsqrt.d   f1, f2         |Floating SQuare RooT (64 bit): Assigns f1 to the square root of f2|
|fsqrt.s   f1, f2         |Floating SQuare RooT: Assigns f1 to the square root of f2|
|fsrm t1      |Write FP rounding mode|
|fsrm t1, t2  |Swap FP rounding mode|
|fsrmi 100     |Write FP rounding mode, immediate|
|fsrmi t1, 100 |Swap FP rounding mode, immediate|
|fssr t1     |Alias for fscsr t1 |
|fssr t1, t2 |Alias for fscsr t1, t2|
|fsub.d    f1, f2, f3     |Floating SUBtract (64 bit): assigns f1 to f2 - f3|
|fsub.s    f1, f2, f3     |Floating SUBtract: assigns f1 to f2 - f3|
|fsw f1,(t2)       |Store Word Coprocessor 1 : Store 32-bit value from f1 to effective memory word address|
|fsw f1,-100       |Store Word Coprocessor 1 : Store 32-bit value from f1 to effective memory word address|
|fsw f1,10000000,t3|Store Word Coprocessor 1 : Store 32-bit value from f1 to effective memory word address using t3 as a temporary|
|fsw f1,label, t3  |Store Word Coprocessor 1 : Store 32-bit value from f1 to effective memory word address using t3 as a temporary|
|j label        |Jump : Jump to statement at label|
|jal label      |Jump And Link: Jump to statement at label and set the return address to ra|
|jalr t0        |Jump And Link Register: Jump to address in t0 and set the return address to ra|
|jalr t0, -100  |Jump And Link Register: Jump to address in t0 and set the return address to ra|
|jr t0          |Jump Register: Jump to address in t0|
|jr t0, -100    |Jump Register: Jump to address in t0|
|la t1,label  |Load Address : Set t1 to label's address|
|lb t1,(t2)     |Load Byte : Set t1 to sign-extended 8-bit value from effective memory byte address|
|lb t1,-100     |Load Byte : Set $1 to sign-extended 8-bit value from effective memory byte address|
|lb t1,10000000 |Load Byte : Set $t1 to sign-extended 8-bit value from effective memory byte address|
|lb t1,label	   |Load Byte : Set $t1 to sign-extended 8-bit value from effective memory byte address|
|lbu t1,(t2)     |Load Byte Unsigned : Set $t1 to zero-extended 8-bit value from effective memory byte address|
|lbu t1,-100     |Load Byte Unsigned : Set $t1 to zero-extended 8-bit value from effective memory byte address|
|lbu t1,10000000 |Load Byte Unsigned : Set t1 to zero-extended 8-bit value from effective memory byte address|
|lbu t1,label	|Load Byte Unsigned : Set t1 to zero-extended 8-bit value from effective memory byte address|
|lh t1,(t2)     |Load Halfword : Set t1 to sign-extended 16-bit value from effective memory halfword address|
|lh t1,-100     |Load Halfword : Set t1 to sign-extended 16-bit value from effective memory halfword address|
|lh t1,10000000 |Load Halfword : Set t1 to sign-extended 16-bit value from effective memory halfword address|
|lh t1,label	   |Load Halfword : Set t1 to sign-extended 16-bit value from effective memory halfword address|
|lhu t1,(t2)     |Load Halfword Unsigned : Set t1 to zero-extended 16-bit value from effective memory halfword address|
|lhu t1,-100     |Load Halfword Unsigned : Set t1 to zero-extended 16-bit value from effective memory halfword address|
|lhu t1,10000000 |Load Halfword Unsigned : Set t1 to zero-extended 16-bit value from effective memory halfword address|
|lhu t1,label	|Load Halfword Unsigned : Set t1 to zero-extended 16-bit value from effective memory halfword address|
|li t1,-100     |Load Immediate : Set t1 to 12-bit immediate (sign-extended)|
|li t1,10000000 |Load Immediate : Set t1 to 32-bit immediate|
|lui t1,%hi(label)     |Load Upper Address : Set t1 to upper 20-bit label's address|
|lw t1,%lo(label)(t2)  |Load from Address|
|lw t1,(t2)     |Load Word : Set t1 to contents of effective memory word address|
|lw t1,-100     |Load Word : Set t1 to contents of effective memory word address|
|lw t1,10000000 |Load Word : Set t1 to contents of effective memory word address|
|lw t1,label	   |Load Word : Set t1 to contents of memory word at label's address|
|mv  t1,t2 |MoVe : Set t1 to contents of t2|
|neg t1,t2 |NEGate : Set t1 to negation of t2|
|nop |NO OPeration|
|not t1,t2 |Bitwise NOT (bit inversion)|
|rdcycle t1    | Read from cycle|
|rdcycleh t1   | Read from cycleh|
|rdinstret t1  | Read from instret|
|rdinstreth t1 | Read from instreth|
|rdtime t1     | Read from time|
|rdtimeh t1    | Read from timeh|
|ret            |Return: return from a subroutine|
|sb t1,(t2)        |Store Byte : Store the low-order 8 bits of t1 into the effective memory byte address|
|sb t1,-100        |Store Byte : Store the low-order 8 bits of $t1 into the effective memory byte address|
|sb t1,10000000,t2 |Store Byte : Store the low-order 8 bits of $t1 into the effective memory byte address|
|sb t1,label,t2    |Store Byte : Store the low-order 8 bits of $t1 into the effective memory byte address|
|seqz t1,t2    |Set EQual to Zero :     if t2 == 0 then set t1 to 1 else 0|
|sgt  t1,t2,t3 |Set Greater Than : if t2 greater than t3 then set t1 to 1 else 0|
|sgtu t1,t2,t3 |Set Greater Than Unsigned : if t2 greater than t3 (unsigned compare) then set t1 to 1 else 0|
|sgtz t1,t2    |Set Greater Than Zero : if t2 >  0 then set t1 to 1 else 0|
|sh t1,(t2)        |Store Halfword : Store the low-order 16 bits of $1 into the effective memory halfword address|
|sh t1,-100        |Store Halfword : Store the low-order 16 bits of $t1 into the effective memory halfword address|
|sh t1,10000000,t2 |Store Halfword : Store the low-order 16 bits of t1 into the effective memory halfword address using t2 as a temporary|
|sh t1,label,t2    |Store Halfword : Store the low-order 16 bits of t1 into the effective memory halfword address using t2 as a temporary|
|sltz t1,t2    |Set Less Than Zero :    if t2 <  0 then set t1 to 1 else 0|
|snez t1,t2    |Set Not Equal to Zero : if t2 != 0 then set t1 to 1 else 0|
|sw t1,(t2)        |Store Word : Store t1 contents into effective memory word address|
|sw t1,-100        |Store Word : Store $t1 contents into effective memory word address|
|sw t1,10000000,t2 |Store Word : Store $t1 contents into effective memory word address using t2 as a temporary|
|sw t1,label,t2    |Store Word : Store $t1 contents into memory word at label's address using t2 as a temporary|
|tail label     |TAIL call: tail call (call without saving return address)a far-away subroutine|


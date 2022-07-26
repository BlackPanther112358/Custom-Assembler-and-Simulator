import matplotlib.pyplot as plt

mem = [0 for i in range(256)]
opcodes = {}
types = {}
register = [0 for i in range(8)]
pc = -1
halted = False
trace = []
# reverse these
# A={"add":"10000", "sub":"10001", "mul":"10110", "xor":"11010","or":"11011", "and":"11100", "addf":"00000", "subf":"00001"}
# B={'10010': 'mov', '11000': 'rs', '11001': 'ls', '00010': 'movf'}
# C={'10011': 'mov', '10111': 'div', '11101': 'not', '11110': 'cmp'}
# D={"ld":"10100", "st":"10101"}
# E={"jmp":"11111", "jlt":"01100", "jgt":"01101", "je":"01111"}
# F={"hlt":"01010"}

dictionary ={'00000':'A','00001':'A','00010':'B','00011':'C','00100':'D','00101':'D','00110':'A','00111':'C','01000':'B','01001':'B','01010':'A','01011':'A','01100':'A','01101':'C','01110':'C','01111':'E','10000':'E','10001':'E','10010':'E','10011':'F'}
      
flags = {"overflow": False, "Less than Flag": False, "Greater than flag": False,"Equal to flag": False}

num = 0
val = 0

# FV(7) , FL(8) , FG(9) , FE(10) is flag register for overflow, less than, greater than, equal to

def reset():
    register[7] = 0

def typeA(op:str, r1:str, r2:str, r3:str):

    val1 = int(r1, 2)
    val2 = int(r2, 2)
    val3 = int(r3, 2)

    #Add
    if(op == "10000"):
        reset()
        register[val3] = register[val2] + register[val1]

        if(register[val3] >= 65536):
            flags["overflow"] = True
            register[val3] %= 65536
        
    #Subtract
    elif(op == "10001"):
        reset()
        if val1 >= val2:
            register[val3] = register[val2] - register[val1]
        else:
            register[val3] = 0  
            flags["overflow"] = True
        
    #Multiply
    elif(op == "10110"):
        reset()
        register[val3] = register[val2] * register[val1]

        if(register[val3] >= 65536):
            flags["overflow"] = True

    #XOR
    elif(op == "11010"):
        reset()
        register[val3] = register[val2] ^ register[val1]

    #OR
    elif(op == "11011"):
        reset()
        register[val3] = register[val2] | register[val1]

    #AND
    elif(op == "11100"):
        reset()
        register[val3] = register[val2] & register[val1]
  
def typeB(op:str, r1:str, imm:str):
    
    val1 = int(r1, 2)
    imm = int(imm,  2)

    #Mov
    if(op == "10010"):
        reset()
        register[val1] = imm

    #LeftShift
    elif(op == "11001"):
        reset()
        register[val1] = val1 << imm

    #RightShift
    elif(op == "11000"):
        reset()
        register[val1] = val1 >> imm

def typeC(op:str, r1:str, r2:str):

    val1 = int(r1, 2)
    val2 = int(r2, 2)

    #Mov Reg
    if(op == "10011"):
        reset()
        register[val1] = register[val2]

    #Divide
    elif(op == "10111"):
        reset()
        register[0] = val1//val2
        register[1] = val1%val2

    #Invert
    elif(op == "11101"):
        temp = val2
        for i in range(16):
            val2 ^= (1 << i)
        
        val1 = val2
        val2 = temp      

    #Compare
    elif(op == "11110"):
        if(val1 > val2):
            num |= (1 << 1)
        
        elif(val1 < val2):
            num |= (1 << 2)
        
        elif(val1 == val2):
            num |= (1 << 0) 

def typeD(op:str, r1:str, mem_addr:str):
    
    val1 = int(r1, 2)
    val_mem = int(mem_addr, 2)

    if(op == "10100"):
        reset()
        register[val1] = mem[val_mem]
        return

    elif(op == "10101"):
        reset()
        mem[val_mem] = register[val1]
        return

def typeE(op:str, mem_addr:str):
    
    global pc
    val_mem = int(mem_addr, 2)

    #unconditional jump
    if(op == "11111"):
        pc = val_mem

    #jump if less
    elif(op == "01100"):
        if(register[7] == 4 or register[7] == 12):
            pc = val_mem

    #jump if greater
    elif(op == "01101"):
        if(register[7] == 2 or register[7] == 10):
            pc = val_mem

    #jump if equal
    elif(op == "01111"):
        if(register[7] == 1 or register[7] == 9):
            pc = val_mem
    
    #return pc

def load_memory():
    for i in range(256):
        try:
            inpt = input()
            if inpt == '':
                continue
            mem[i] = int(inpt, 2)
        except EOFError:
            break
        except Exception:
            break
    return

def process_inst(inst:int):
    k = str(inst)
    op = k[0:5]
    mytype = dictionary[op]
    global halted
    if(mytype == 'A'):
        typeA(op, k[7:10], k[10:13], k[13:16])

    elif(mytype == 'B'):
        typeB(op, k[5:8], k[8:16])

    elif(mytype == 'C'):
        typeC(op, k[10:13], k[13:16])
    
    elif(mytype == 'D'):
        typeD(op, k[5:8], k[8:16])

    elif(mytype == 'E'):
        typeE(op, k[8:16])

    elif(op == '01010'):
        halted = True

def out_state(pc:int):
    print(pc, end = ' ')
    for reg in register:
        print(bin(reg)[2::], end = ' ')
    print()
    return

def out_mem():
    for line in mem:
        print(bin(line)[2::])
    return

def update_cycledata(pc:int):  #For q4
    trace.append(pc)
    return

def plot_scatter():
    plt.ylabel('Cycle No.')
    plt.scatter(trace, [i for i in range(len(trace))])
    plt.show()
    return

def main():
    load_memory()
    while(not halted):
        pc += 1
        inst = mem[pc]
        process_inst(inst)
        out_state(pc)
        update_cycledata(pc)
    out_mem()
    plot_scatter()
    return

main()
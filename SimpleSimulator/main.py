mem = [0 for i in range(256)]
opcodes = {}
types = {}
register = [0 for i in range(8)]
pc = -1
halted = False
# reverse these
A={"add":"10000", "sub":"10001", "mul":"10110", "xor":"11010","or":"11011", "and":"11100", "addf":"00000", "subf":"00001"}
B={'10010': 'mov', '11000': 'rs', '11001': 'ls', '00010': 'movf'}
C={'10011': 'mov', '10111': 'div', '11101': 'not', '11110': 'cmp'}
D={"ld":"10100", "st":"10101"}
E={"jmp":"11111", "jlt":"01100", "jgt":"01101", "je":"01111"}
F={"hlt":"01010"}

flags = {"overflow": False, "Less than Flag": False, "Greater than flag": False,"Equal to flag": False}

num = 0
val = 0

def reset():
    register[7] = 0
    
def typeA(op:str, r1:str, r2:str, r3:str):

    val3 = int(r1, 2)
    val2 = int(r2, 2)
    val1 = int(r3, 2)

    #Add
    if(op == "10000"):
        register[7] = 0
        register[val3] = register[val2] + register[val1]

        if(register[val3] >= 65536):
            flags["overflow"] = True
            register[val3] %= 65536
        
    #Subtract
    elif(op == "10001"):
        register[7] = 0
        if val1 >= val2:
            register[val3] = register[val2] - register[val1]
        else:
            register[val3] = 0  
            flags["overflow"] = True
        
    #Multiply
    elif(op == "10110"):
        register[7] = 0
        register[val3] = register[val2] * register[val1]

        if(register[val3] >= 65536):
            flags["overflow"] = True

    #XOR
    elif(op == "11010"):
        register[7] = 0
        register[val3] = register[val2] ^ register[val1]

    #OR
    elif(op == "11011"):
        register[7] = 0
        register[val3] = register[val2] | register[val1]

    #AND
    elif(op == "11100"):
        register[7] = 0
        register[val3] = register[val2] & register[val1]
  
def typeB(op:str, r1:str, imm:str):
    
    val1 = int(r1, 2)
    imm = int(imm,  2)

    #Mov
    if(op == "10010"):
        register[7] = 0
        register[val1] = imm

    #LeftShift
    elif(op == "11001"):
        register[7] = 0
        register[val1] = val1 << imm

    #RightShift
    elif(op == "11000"):
        register[7] = 0
        register[val1] = val1 >> imm

def typeC(op:str, r1:int, r2:int):

    val1 = int(r1, 2)
    val2 = int(r2, 2)

    #Mov Reg
    if(op == "10011"):
        register[7] = 0
        register[val1] = register[val2]

    #Divide
    elif(op == "10111"):
        register[7] = 0
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

def typeD(op:str, r1:int, mem_addr:int):
    return

def typeE(op:str, mem_addr:int):
    return

def load_memory():
    return

def process_inst(inst:int):
    return

def out_state():
    return

def out_mem():
    return

def update_metadata():  #For q4
    return

def main():
    load_memory()
    while(not halted):
        pc += 1
        inst = mem[pc]
        process_inst(inst)
        out_state()
        update_metadata()
    out_mem()
    return

main()
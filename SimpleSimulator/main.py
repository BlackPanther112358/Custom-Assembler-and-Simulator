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

flags = {"overflow": False}


def typeA(op:str, r1:str, r2:str, r3:str):

    val3 = bin(int(r1))[2:]
    val2 = bin(int(r2))[2:]
    val1 = bin(int(r3))[2:]

    #Add
    if(op == "10000"):
        register[val3] = register[val2] + register[val1]

        if(len(str(int(val3,2))) > 3):
            flags["overflow"] = True
        return

    #Subtract
    elif(op == "10001"):
        if val1 >= val2:
            register[val3] = register[val2] + register[val1]
        else:
            register[val3] = 0  
            flags["overflow"] = True
        return

    #Multiply
    if(op == "10110"):
        register[val3] = register[val2] * register[val1]

        if(len(str(int(val3,2))) > 3):
            flags["overflow"] = True
        return

    #XOR
    if(op == "11010"):
        register[val3] = register[val2] ^ register[val1]
        return

    #OR
    if(op == "11011"):
        register[val3] = register[val2] | register[val1]
        return

    #AND
    if(op == "11100"):
        register[val3] = register[val2] & register[val1]
        return
  
def typeB(op:str, r1:str, imm:str):
    
    val1 = bin(int(r1))[2:]
    imm = bin(int(imm))[2:]

    #Mov
    if(op == "10010"):
        register[val1] = imm
        return

    #LeftShift
    if(op == "11001"):
        register[val1] = val1 << imm
        return

    #RightShift
    if(op == "11000"):
        register[val1] = val1 >> imm
        return

def typeC(op:str, r1:int, r2:int):
    return

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
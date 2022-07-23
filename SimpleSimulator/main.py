import matplotlib.pyplot as plt

mem = [0 for i in range(256)]
opcodes = {}
types = {}
register = [0 for i in range(8)]
pc = -1
halted = False
trace = []
# reverse these
A={"add":"10000", "sub":"10001", "mul":"10110", "xor":"11010","or":"11011", "and":"11100", "addf":"00000", "subf":"00001"}
B={'10010': 'mov', '11000': 'rs', '11001': 'ls', '00010': 'movf'}
C={'10011': 'mov', '10111': 'div', '11101': 'not', '11110': 'cmp'}
D={"ld":"10100", "st":"10101"}
E={"jmp":"11111", "jlt":"01100", "jgt":"01101", "je":"01111"}
F={"hlt":"01010"}

def typeA(op:str, r1:int, r2:int, r3:int):
    return

def typeB(op:str, r1:int, imm:int):
    return

def typeC(op:str, r1:int, r2:int):
    return

def typeD(op:str, r1:int, mem_addr:int):
    return

def typeE(op:str, mem_addr:int):
    return

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
    return

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
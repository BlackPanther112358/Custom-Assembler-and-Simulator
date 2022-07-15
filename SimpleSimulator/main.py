mem = [0 for i in range(256)]
opcodes = {}
types = {}
register = [0 for i in range(8)]
pc = -1
halted = False

def add(r1:int, r2:int, r3:int):
    return r1 + r2 + r3

def sub(r1:int, r2:int, r3:int):
    return

def mul(r1:int, r2:int, r3:int):
    return

def or_(r1:int, r2:int, r3:int):
    return

def xor(r1:int, r2:int, r3:int):
    return

def and_(r1:int, r2:int, r3:int):
    return

def addf(r1:int, r2:int, r3:int):
    return

def subf(r1:int, r2:int, r3:int):
    return

ISA = {'10000': 'A', '10001': 'A', '10110': 'A', '11010': 'A', '11011': 'A', '11100': 'A', '00000': 'A', '00001': 'A', '10010': 'B', '11000': 'B', '11001': 'B', '00010': 'B', '10011': 'C', '10111': 'C', '11101': 'C', '11110': 'C', '10100': 'D', '10101': 'D', '11111': 'E', '01100': 'E', '01101': 'E', '01111': 'E', '01010': 'F'}
syntax = {'A' : ['reg', 'reg', 'reg'], 'B' : ['reg', 'imm'], 'C' : ['reg', 'reg'], 'D' : ['reg', 'mem'], 'E' : ['mem'], 'F' : []}
# A={'10000': 'add', '10001': 'sub', '10110': 'mul', '11010': 'xor', '11011': 'or', '11100': 'and', '00000': 'addf', '00001': 'subf'}
A={'10000': add, '10001': sub, '10110': mul, '11010': xor, '11011': or_, '11100': and_, '00000': addf, '00001': subf}
# B={'10010': 'mov', '11000': 'rs', '11001': 'ls', '00010': 'movf'}
# C={'10011': 'mov', '10111': 'div', '11101': 'not', '11110': 'cmp'}
# D={'10100': 'ld', '10101': 'st'}
# E={"11111":"jmp", "01100":"jlt", "01101":"jgt", "01111":"je"}
# F={"01010":"hlt"}

# def typeA(op:str, r1:int, r2:int, r3:int):
#     return

# def typeB(op:str, r1:int, imm:int):
#     return

# def typeC(op:str, r1:int, r2:int):
#     return

# def typeD(op:str, r1:int, mem_addr:int):
#     return

# def typeE(op:str, mem_addr:int):
#     return

def load_memory()->list:
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
    # Convert inst to string using bin
    #Extract opcode
    #Use disctionary to find correct function to call and use ISA to find syntax
    return

def out_state():
    return

def out_mem():
    return

def update_metadata(cycle_cnt:int, pc:int):  #For q4
    return

def main():
    load_memory()
    cycle_cnt = 0
    while(not halted):
        pc += 1
        inst = mem[pc]
        process_inst(inst)
        out_state()
        update_metadata(cycle_cnt, pc)
        cycle_cnt += 1
    out_mem()
    return

main()
import math
import matplotlib.pyplot as plt
# import sys

mem = [0 for i in range(256)]
opcodes = {}
types = {}
register = [0 for i in range(8)]
new_pc = -1
pc = -1
halted = False
trace = []


def dec_2_bin(num:float)->str:
    a=str(num)
    before=""
    after=""
    flag=True
    for i in a:
        if(i=='.'):
            flag=False
        if(flag):
            before+=i
        else:
            after+=i
    if(flag):
        return "0"
    before=str(bin(int(before))[2::])
    after=float(after)
    temp=""
    while(after!=0):
        after*=2
        temp+=str(int(after))
        after=after-int(after)
    if(len(before)>8 or before=="0" or len(before)-1+len(temp)>5):
        return "0"
    ans=""
    x=len(bin(len(before)-1)[2::])
    for i in range(3-x):
        ans+="0"
    ans+=bin(len(before)-1)[2::]+before[1::]+temp
    for i in range(8-len(ans)):
        ans+="0"
    return ans
    
def bin_2_dec(num:str)->float:
    exp=int(num[:3:],2)
    ans="1"
    for i in range(exp):
        if(3+i<8):
            ans+=num[i+3]
        else:
            ans+="0"
    ans=int(ans,2)
    j=-1
    for i in range(exp+3,8):
        ans+=int(num[i])*math.pow(2,j)
        j-=1
    return ans

dictionary = {'10000': 'A', '10001': 'A', '10110': 'A', '11010': 'A', '11011': 'A','11100': 'A','00000': 'A', '00001': 'A','10010': 'B','11000': 'B','11001': 'B', '00010': 'B',  '10011': 'C', '10111': 'C', '11101': 'C', '11110': 'C', '10100': 'D', '10101': 'D','11111': 'E', '01100': 'E', '01101': 'E', '01111': 'E', '01010': 'F'}

# flags = {"overflow": False, "Less than Flag": False, "Greater than flag": False,"Equal to flag": False}

# FV(7) , FL(8) , FG(9) , FE(10) is flag register for overflow, less than, greater than, equal to

num = 0
val = 0

def cust_bin(inpt:int, mylen:int)->str:
    bin_val:str = bin(inpt)[2::]
    bin_val = (mylen - len(bin_val))*'0' + bin_val
    return bin_val

def reset():
    register[7] = 0

def typeA(op:str, r1:str, r2:str, r3:str):

    val1 = int(r1, 2)
    val2 = int(r2, 2)
    val3 = int(r3, 2)

    global register

    # print(f"{register[val1]} : {val1}")
    # print(f"{register[val2]} : {val2}")
    # print(f"{register[val3]} : {val3}")
    #Add
    if(op == "10000"):
        reset()
        register[val3] = register[val2] + register[val1]

        if(register[val3] >= 65536):
            register[7] |= (1 << 3)
            register[val3] %= 65536
        
    #Subtract
    elif(op == "10001"):
        reset()
        if register[val1] >= register[val2]:
            register[val3] = register[val2] - register[val1]
        else:
            register[val3] = 0  
            register[7] |= (1 << 3)
        
    #Multiply
    elif(op == "10110"):
        reset()
        register[val3] = register[val2] * register[val1]

        if(register[val3] >= 65536):
            register[7] |= (1 << 3)

    #XOR
    elif(op == "11010"):
        reset()
        for i in range(16):
            if register[val1]&(1<<i) ^ register[val2]&(1<<i):
                register[val3] |=(1<<i)
            elif register[val3]&(1<<i):
                register[val3] ^=(1<<i)

    #OR
    elif(op == "11011"):
        reset()
        register[val3] = 0
        for i in range(16):
            if register[val1]&(1<<i) | register[val2]&(1<<i):
                register[val3] |= (1<<i)

    #AND
    elif(op == "11100"):
        reset()
        register[val3] = 0
        for i in range(16):
            if register[val1]&(1<<i) & register[val2]&(1<<i):
                register[val3] |= (1<<i)

    #ADDF
    elif(op == "00000"):
        reset()
        temp1=cust_bin(register[val1],8)
        temp2=cust_bin(register[val2],8)
        x=dec_2_bin(bin_2_dec(temp1)+bin_2_dec(temp2))
        if(x=="0"):
            register[val3]=0
            register[7] |= (1 << 3)
        else:
            register[val3]=x

    #SUBF
    elif(op == "00001"):
        reset()
        temp1=cust_bin(register[val1],8)
        temp2=cust_bin(register[val2],8)
        x=dec_2_bin(bin_2_dec(temp2)-bin_2_dec(temp1))
        if(x=="0"):
            register[val3]=0
            register[7] |= (1 << 3)
        else:
            register[val3]=x



        
def typeB(op:str, r1:str, imm:str):
    
    val1 = int(r1,2)
    imm = int(imm,2)

    #Mov
    if(op == "10010"):
        reset()
        register[val1] = imm

    #LeftShift
    elif(op == "11001"):
        reset()
        register[val1] = register[val1] << imm

    #RightShift
    elif(op == "11000"):
        reset()
        register[val1] = register[val1] >> imm

    #MOVF
    elif(op=="00010"):
        reset()
        register[val1]=imm

def typeC(op:str, r1:str, r2:str):

    val1 = int(r1, 2)
    val2 = int(r2, 2)

    #Mov Reg
    if(op == "10011"):
        register[val2] = register[val1]
        reset()

    #Divide
    elif(op == "10111"):
        reset()
        register[0] = register[val1]//register[val2]
        register[1] = register[val1]%register[val2]

    #Invert
    elif(op == "11101"):
        register[val2] = register[val1]
        for i in range(16):
            register[val2] ^= (1 << i)

    #Compare
    elif(op == "11110"):
        if(register[val1] > register[val2]):
            register[7] |= (1 << 1)
        
        elif(register[val1] < register[val2]):
            register[7] |= (1 << 2)
        
        elif(register[val1] == register[val2]):
            register[7] |= (1 << 0) 

def typeD(op:str, r1:str, mem_addr:str):
    
    val1 = int(r1, 2)
    val_mem = int(mem_addr, 2)

    #load
    if(op == "10100"):
        reset()
        register[val1] = mem[val_mem]
        return

    #store
    elif(op == "10101"):
        reset()
        mem[val_mem] = register[val1]
        return

def typeE(op:str, mem_addr:str):
    
    global new_pc
    val_mem = int(mem_addr, 2)

    #unconditional jump
    if(op == "11111"):
        new_pc = val_mem -1
        reset()

    #jump if less
    elif(op == "01100"):
        if(register[7] == 4 or register[7] == 12):
            new_pc = val_mem -1
        reset()

    #jump if greater
    elif(op == "01101"):
        if(register[7] == 2 or register[7] == 10):
            new_pc = val_mem -1
        reset()

    #jump if equal
    elif(op == "01111"):
        if(register[7] == 1 or register[7] == 9):
            new_pc = val_mem -1
        reset()

def load_memory():
    # sys.stdin = open('input.txt', 'r')
    # sys.stdout = open('output.txt', 'w')
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
    k = cust_bin(inst, 16)
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
        reset()

def out_state(pc:int):
    print(cust_bin(pc, 8), end = ' ')
    for reg in register:
        print(cust_bin(reg, 16), end = ' ')
    print()
    return

def out_mem():
    for line in mem:
        print(cust_bin(line, 16))
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
    # sys.stdout = open('output.txt', 'w')
    load_memory()
    #global halted
    while(not halted):
        global pc
        global new_pc
        pc += 1
        inst = mem[pc]
        process_inst(inst)
        out_state(pc)
        update_cycledata(pc)
        if (new_pc != -1):
            pc = new_pc
            new_pc = -1
    out_mem()
    plot_scatter()
    return

main()

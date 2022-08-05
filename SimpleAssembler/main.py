import math

ISA = {'add' : ['A'], 'sub' : ['A'], 'mov' : ['B', 'C'], 'ld' : ['D'], 'st' : ['D'], 'mul' : ['A'], 'div' : ['C'], 'ls' : ['B'], 'rs' : ['B'], 'or' : ['A'], 'xor' : ['A'], 'and' : ['A'], 'not' : ['C'], 'cmp' : ['C'], 'jmp' : ['E'], 'jgt' : ['E'], 'jlt' : ['E'], 'je' : ['E'], 'hlt' : ['F'], 'addf' : ['A'], 'subf' : ['A'], 'movf' : ['B']}
syntax = {'A' : ['reg', 'reg', 'reg'], 'B' : ['reg', 'imm'], 'C' : ['reg', 'reg'], 'D' : ['reg', 'mem'], 'E' : ['mem'], 'F' : []}
errors = {'Undefined variable' : [], 'Invalid Register address' : [], 'Invalid Instruction' : [], 'Undefined label' : [], 'Invalid operation on FLAG register' : [], 'Invalid immediate value' : [], 'Cannot use label as variable' : [], 'Cannot use variable as label' : [], 'Variables not declared' : [], 'Missing halt instruction' : [], 'Halt instruction not at the end' : [], 'General Syntax Error' : [], 'Memory overflow' : []}
vars = []
labels = []

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

def input_instructions()->list[int, str]:     #Function to take input from termimal
    lines = []
    cnt:int = 1
    while True:
        try:
            inpt = input()
            if inpt == '':
                continue
            lines.append([cnt, inpt])
            cnt += 1
        except Exception:
            break
    return lines

def process_var_lab(inpt:list[int, str])->list:   #Function to scan input for variables and labels and store them
    inpt_var = True
    ret_list = []
    for num, line in inpt:
        args = line.split()
        if(len(args) == 0):
            continue
        if(args[0] == 'var'):
            if inpt_var is False:
                errors['General Syntax Error'].append(num)
            if(len(args) != 2):
                errors['General Syntax Error'].append(num)
            else:
                vars.append(args[1])
            continue
        elif(args[0][-1] == ':'):
            if(len(args[0]) == 1):
                errors['General Syntax Error'].append(num)
            else:
                labels.append(args[0][:-1])
                args = args[1::]
        inpt_var = False
        if(len(args) == 0):
            errors['General Syntax Error'].append(num)
            continue
        ret_list.append([num, ' '.join(args)])
    return ret_list

def check_syntax(num:int, type:str, args:list)->bool:    #Function to check the syntax of each incidividual line, with its type (A ... F)
    inst = args[0]
    args = args[1::]
    if(len(args) != len(syntax[type])):
        errors['General Syntax Error'] = True
        return
    syn = syntax[type]
    check = True
    for i in range(len(args)):
        if syn[i] == 'reg':
            if args[i] == "FLAGS":
                if (inst == 'mov') and (i == 0):
                    pass
                else:
                    errors['Invalid operation on FLAG register'].append(num)
                    check = False
            else:
                if len(args[i]) == 2:
                    try:
                        if (args[i][0] == 'R') and (int(args[i][1]) in range(0, 7)):
                            pass
                        else:
                            errors['Invalid Register address'].append(num)
                            check = False
                    except Exception:
                        errors['Invalid Register address'].append(num)
                        check = False
                else:
                    errors['Invalid Register address'].append(num)
                    check = False
        elif syn[i] == 'imm':
            if(args[i][0] != '$'):
                errors['Invalid immediate value'].append(num)
                check = False
            else:
                try:
                    num = int(args[i][1::])
                    if num not in range(0, 256):
                        errors['Invalid immediate value'].append(num)
                        check = False
                except Exception:
                    errors['Invalid immediate value'].append(num)
                    check = False
        else:
            if type == 'D':
                if args[i] not in vars:
                    if(args[i] in labels):
                        errors['Cannot use label as variable'].append(num)
                        check = False
                    else:
                        errors['Undefined variable'].append(num)
                        check = False
            else:
                if args[i] not in labels:
                    if(args[i] in vars):
                        errors['Cannot use variable as label'].append(num)
                        check = False
                    else:
                        errors['Undefined label'].append(num)
                        check = False
    if check:
        return True
    return False

def take_input()->list:         #Function to take input and check for any possible errors
    raw_inpt = input_instructions()
    if len(raw_inpt) > 256:
        errors['Memory overflow'] = True
    inpt = process_var_lab(raw_inpt)
    halt_obs = False            #checks if halt command has been encountered
    for num, line in inpt:
        if halt_obs:
            errors['Halt instruction not at the end'] = True
            halt_obs = False
        args = line.split()
        if(args[0] not in ISA):
            errors['Invalid Instruction'] = True
            continue
        pos_types = ISA[args[0]]    #Fetches the possibles types of instrctions for the command (mov has 2 possible)
        if len(pos_types) == 1:
            check_syntax(num, pos_types[0], args)
        else:
            if len(args) != 3:
                errors['General Syntax Error'] = True
            else:
                if '$' in args[2]:
                    check_syntax(num, 'B', args)
                else:
                    check_syntax(num, 'C', args)
        if pos_types[0] == 'F':
            halt_obs = True
    if not(halt_obs) and not(errors['Halt instruction not at the end']):
        errors['Missing halt instruction'] = True
    # if(True in errors.values()):    #Raises exception with all the errors detected
    #     raise Exception(
    #         [Exception(i) for i in errors if errors[i]]
    #     )
    if(sum(errors.values()) > 0):
        exceptions = []
        for error in errors:
            if(errors[error] > 0):
                for line in errors[error]:
                    exceptions.append(f'{error} at line no. {line}')
        raise Exception(
            exceptions
        )
    return raw_inpt

def convert(inpt:list)->list:
    #Dictionaries corresponding to various types of instructions
    A={"add":"10000", "sub":"10001", "mul":"10110", "xor":"11010","or":"11011", "and":"11100", "addf":"00000", "subf":"00001"}
    B={"mov":"10010", "rs":"11000", "ls":"11001", "movf":"00010"}
    C={"mov":"10011", "div":"10111", "not":"11101", "cmp":"11110"}
    D={"ld":"10100", "st":"10101"}
    E={"jmp":"11111", "jlt":"01100", "jgt":"01101", "je":"01111"}
    F={"hlt":"01010"}
    reg={"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110", "FLAGS":"111"}
    var=[] #Stores the names of variables
    code=[]
    for i in inpt:
        lst=i.split()
        if(lst[0]=="var"): #If the line is a variable line
            var.append(lst[1]) #Store its name
        else:
            code.append(i)
    labels={}
    for i in range(len(code)):
        lst=code[i].split()
        if(lst[0][-1]==':'):
            labels[lst[0]]=i
    exec=[] #Executable file (holds binary information)
    for i in code:
        s=""
        lst=i.split()
        x=0
        if(lst[0][-1]==':'):
            x=1
        if(lst[x] in A): #A type
            s=A.get(lst[x])+"00"+reg.get(lst[x+1])+reg.get(lst[x+2])+reg.get(lst[x+3])
        elif(lst[x] in B and lst[x+2][0]=='$'): #B type
            s=B.get(lst[x+0])+reg.get(lst[x+1])
            lst[x+2]=lst[x+2][1::] #Takes the number without dollar sign
            a=""
            for i in range(8-len(bin(int(lst[x+2]))[2::])): #Bits in the number that are unused (out of 8)
                a+="0"
            a+=bin(int(lst[x+2]))[2::] #Appends the binary representation of immediate
            s+=a
        elif(lst[x+0] in C): #C type
            s=C.get(lst[x+0])+"00000"+reg.get(lst[x+1])+reg.get(lst[x+2])
        elif(lst[x+0] in D): #D type
            s=D.get(lst[x+0])+reg.get(lst[x+1])
            idx=var.index(lst[x+2]) #Index of variable (on which position was it encountered)
            a=""
            for i in range(8-len(bin(idx+len(code))[2::])): #Bits in the number that are unused (out of 8)
                a+="0"
            a+=bin(idx+len(code))[2::] #Appends the binary representation of immediate
            s+=a
        elif(lst[x+0] in E): #E type
            s=E.get(lst[x+0])+"000"
            idx=labels.get(lst[x+1]+':') #Index of variable (on which position was it encountered)
            a=""
            for i in range(8-len(bin(int(idx))[2::])): #Bits in the number that are unused (out of 8)
                a+="0"
            a+=bin(idx)[2::] #Appends the binary representation of immediate
            s+=a
        else: #F type
            s=F.get(lst[x+0])+"00000000000"
        exec.append(s) #Appends the binary of each instruction in the executable
    return exec

def output(ans:list):
    for line in ans:
        print(line)

def main():
    ans = take_input()
    ans = convert(ans)
    output(ans)
    
main()
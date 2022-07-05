def take_input()->list:
    return
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
    return

def main():
    ans = take_input()
    ans = convert(ans)
    output(ans)

if '__name__' == '__main__':
    main()


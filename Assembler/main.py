def take_input()->list:
    return

def convert(inpt:list)->list:
    #Dictionaries corresponding to various types of instructions
    A={"add":"10000", "sub":"10001", "mul":"10110", "xor":"11010","or":"11011", "and":"11100", "addf":"00000"}
    B={"mov":"10010", "rs":"11000", "ls":"11001", "subf":"00001"}
    C={"mov":"10011", "div":"10111", "not":"11101", "cmp":"11110",}
    D={"ld":"10100", "st":"10101"}
    E={"jmp":"11111", "jlt":"01100", "jgt":"01101", "je":"01111"}
    F={"hlt":"01010", "movf":"00010"}
    reg={"R0":"000", "R1":"001", "R2":"010", "R3":"011", "R4":"100", "R5":"101", "R6":"110"}
    count=0 #Counts the number of instructions (exculding Var X lines)
    var=[] #Stores the names of variables
    for i in inpt:
        lst=i.split()
        if(lst[0][0]=='v'): #if the line is a variable line
            var.append(i.split()[1]) #Store its name
        else:
            count+=1 #else count the number of lines
    exec=[] #Executable file (holds binary information)
    for i in inpt:
        s=""
        lst=i.split()
        if(lst[0]=="var"): #Skip instruction if it is variable declaration
            continue
        elif(lst[0] in A): #A type
            s=A.get(lst[0])+"00"+reg.get(lst[1])+reg.get(lst[2])+reg.get(lst[3])
        elif(lst[0] in B): #B type
            s=B.get(lst[0])+reg.get(lst[1])
            lst[2]=lst[2][1::] #Takes the number without dollar sign
            a=""
            for i in range(8-len(bin(int(lst[2]))[2::])): #Bits in the number that are unused (out of 8)
                a+="0"
            a+=bin(int(lst[2]))[2::] #Appends the binary representation of immediate
            s+=a
        elif(lst[0] in C): #C type
            s=C.get(lst[0])+"00000"+reg.get(lst[1])+reg.get(lst[2])
        elif(lst[0] in D): #D type
            s=D.get(lst[0])+reg.get(lst[1])
            idx=var.index(lst[2]) #Index of variable(on which position was it encountered)
            a=""
            for i in range(8-len(bin(idx+count)[2::])): #Bits in the number that are unused (out of 8)
                a+="0"
            a+=bin(idx+count)[2::] #Appends the binary representation of immediate
            s+=a
        elif(lst[0] in E): #E type
            s=E.get(lst[0])+"000"
            idx=var.index(lst[1]) #Index of variable(on which position was it encountered)
            a=""
            for i in range(8-len(bin(idx+count)[2::])): #Bits in the number that are unused (out of 8)
                a+="0"
            a+=bin(idx+count)[2::] #Appends the binary representation of immediate
            s+=a
        else: #F type
            s=F.get(lst[0])+"00000000000"
        exec.append(s) #Appends the binary of each instruction in the executable
    return exec #returns executable file

def output(ans:list):
    return

def main():
    ans = take_input()
    ans = convert(ans)
    output(ans)

if '__name__' == '__main__':
    main()


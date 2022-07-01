ISA = {'add' : ['A'], 'sub' : ['A'], 'mov' : ['B', 'C'], 'ld' : ['D'], 'st' : ['D'], 'mul' : ['A'], 'div' : ['C'], 'ls' : ['B'], 'rs' : ['B'], 'or' : ['A'], 'xor' : ['A'], 'and' : ['A'], 'not' : ['C'], 'cmp' : ['C'], 'jmp' : ['E'], 'jgt' : ['E'], 'jlt' : ['E'], 'je' : ['E'], 'hlt' : ['F']}
syntax = {'A' : ['reg', 'reg', 'reg'], 'B' : ['reg', 'imm'], 'C' : ['reg', 'reg'], 'D' : ['reg', 'mem'], 'E' : ['mem'], 'F' : []}
errors = {'Undefined variable' : False, 'Invalid Register address' : False, 'Invalid Instruction' : False, 'Undefined label' : False, 'Invalid operation on FLAG register' : False, 'Invalid immediate value' : False, 'Cannot use label as variable' : False, 'Cannot use variable as label' : False, 'Variables not declared' : False, 'Missing halt instruction' : False, 'Halt instruction not at the end' : False, 'General Syntax Error' : False}
vars = []
labels = []

def input_instructions()->list:
    lines = []
    while True:
        try:
            inpt = input()
            if inpt == '':
                continue
            lines.append(inpt)
        except Exception:
            break
    return

def process_var_lab(inpt:list)->list:
    inpt_var = True
    ret_list = []
    for line in inpt:
        args = line.split()
        if(len(args) == 0):
            continue
        if(args[0] == 'var'):
            if inpt_var is False:
                errors['General Syntax Error'] = True
            if(len(args) != 2):
                errors['General Syntax Error'] = True
            else:
                vars.append(args[1])
            continue
        elif(args[0][-1] == ':'):
            labels.append(args[0][:-1])
            args = args[1::]
        inpt_var = False
        if(len(args) == 0):
            errors['General Syntax Error'] = True
            continue
        ret_list.append(' '.join(args))
    return ret_list

def check_syntax(type:str, args:list)->bool:
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
                if (inst == 'mov') and (i == 1):
                    pass
                else:
                    errors['Invalid operation on FLAG register'] = True
                    check = False
            else:
                if len(args[i]) == 2:
                    try:
                        if (args[0] == 'R') and (int(args[1]) in range(0, 7)):
                            pass
                        else:
                            errors['Invalid Register address'] = True
                            check = False
                    except Exception:
                        errors['Invalid Register address'] = True
                        check = False
                else:
                    errors['Invalid Register address'] = True
                    check = False
        elif syn[i] == 'imm':
            if(args[i][0] != '$'):
                errors['Invalid immediate value'] = True
                check = False
            else:
                try:
                    num = int(args[i][1::])
                    if num not in range(0, 256):
                        errors['Invalid immediate value'] = True
                        check = False
                except Exception:
                    errors['Invalid immediate value'] = True
                    check = False
        else:
            if type == 'D':
                if args[i] not in vars:
                    errors['Undefined variable'] = True
                    check = False
            else:
                if args[i] not in labels:
                    errors['Undefined label'] = True
                    check = False
    if check:
        return True
    return False

def take_input()->list:
    inpt = input_instructions()
    inpt = process_var_lab(inpt)
    halt_obs = False
    for line in inpt:
        if halt_obs:
            errors['Halt instruction not at the end'] = True
            halt_obs = False
        args = line.split()
        if(args[0] not in ISA):
            errors['Invalid Instruction'] = True
            continue
        pos_types = ISA[args[0]]
        if len(pos_types) == 1:
            check_syntax(pos_types[0], args)
        else:
            if len(args) != 3:
                errors['General Syntax Error'] = True
            else:
                if '$' in args[2]:
                    check_syntax('B', args)
                else:
                    check_syntax('C', args)
        if type == 'F':
            halt_obs = True
    if not(halt_obs) and not(errors['Halt instruction not at the end']):
        errors['Missing halt instruction'] = True
    if(True in errors.values()):
        raise Exception(
            [Exception(i) for i in errors if errors[i]]
        )
    return inpt

def convert(inpt:list)->list:
    return 

def output(ans:list):
    return

def main():
    ans = take_input()
    ans = convert(ans)
    output(ans)

if '__name__' == '__main__':
    main()


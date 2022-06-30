ISA = {'add' : ['A'], 'sub' : ['A'], 'mov' : ['B', 'C'], 'ld' : ['D'], 'st' : ['D'], 'mul' : ['A'], 'div' : ['C'], 'ls' : ['B'], 'rs' : ['B'], 'or' : ['A'], 'xor' : ['A'], 'and' : ['A'], 'not' : ['C'], 'cmp' : ['C'], 'jmp' : ['E'], 'jgt' : ['E'], 'jlt' : ['E'], 'je' : ['E'], 'hlt' : ['F']}
syntax = {}
errors = {'Undefined variable' : False, 'Invalid Register address' : False, 'Invalid Instruction' : False, 'Undefined label' : False, 'Invalid operation on FLAG register' : False, 'Invalid immediate value' : False, 'Cannot use label as variable' : False, 'Cannot use variable as label' : False, 'Variables not declared' : False, 'Missing halt instruction' : False, 'Halt instruction not at the end' : False, 'General Syntax Error' : False}
vars = []
labels = []

def input_instructions()->list:
    return

def take_input()->list:
    inpt = input_instructions()

    return

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


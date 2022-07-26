import platform

mem_size: int
add_type: str

nibble_size: int = 4
byte_size: int = 8
word_size: int = int(platform.architecture()[0][:-3])

conversions: dict = {'':0, 'da':1, 'h':2, 'k':3, 'M':6, 'G':9, 'T':12, 'P':15, 'E':18}

def inpt_int()->int:
    """Function to take input integer"""
    try_cnt = 0
    while try_cnt < 3:
        try_cnt += 1
        try:
            inpt = int(input('Please enter: '))
            if inpt > 0:
                return inpt
            print('Please enter a positive integer')
        except:
            print('Invalid input entered')
    print('Program terminated due to multiple incorrect inputs')    
    return -1

def inpt_option(poss:int)->int:
    """Function to take input for the option for menu based program"""
    try_cnt = 0
    while try_cnt < 3:
        try_cnt += 1
        try:
            inpt = int(input('Please choose an option: '))
            if inpt in range(1, poss + 1):
                return inpt
            print('Please enter a valid option')
        except:
            print('Invalid input entered')
    print('Program terminated due to multiple incorrect inputs')    
    return -1

def inpt_mem()->int:
    """Function to take input for memory space input from terminal and return in number of bits"""
    try_cnt = 0
    while(try_cnt < 3):
        try_cnt += 1
        try:
            inpt = input('Enter the size of memory: ')
            val, unit = inpt.split()
            val = int(val)
            if(unit[-1] == 'b'):
                pass
            elif(unit[-1] == 'B'):
                val *= 8
            else:
                print('Please enter value in bits or Bytes')
                continue
            unit = unit[:-1]
            if unit not in conversions:
                print('Invalid prefix entered')
            val *= pow(10, conversions[unit])
            return val
        except:
            print('Invalid input entered')
            continue
    print('Program terminated due to multiple incorrect inputs')
    return -1

def inpt_add_type()->str:
    """"Function to take input for how the memory is being addressed"""
    try_cnt = 0
    while try_cnt < 3:
        try_cnt += 1
        try:
            inpt = input('Enter the type: ')
            inpt = inpt.lower()
            if inpt in ['bit', 'nibble', 'byte', 'word']:
                return inpt
            print('Please enter the input in valid format')
        except:
            print('Invalid input')
    print('Program terminated due to multiple incorrect inputs') 
    return 'Invalid'

def first_ques()->None:
    """Function to handle first question"""
    inst_size = inpt_int()
    if inst_size == -1:
        return
    reg_size = inpt_int()
    if reg_size == -1:
        return
    add_cnt: int = mem_size
    match add_cnt:
        case 'byte':
            add_cnt = (add_cnt + byte_size - 1)//byte_size
        case 'nibble':
            add_cnt = (add_cnt + nibble_size - 1)//nibble_size
        case 'word':
            add_cnt = (add_cnt + word_size - 1)//word_size
    add_size: int = 0
    while((1<<add_size) < add_cnt):
        add_size += 1
    if (add_size + reg_size) > inst_size:
        print('Length of instruction too small')
        return
    op_size: int = inst_size - add_size - reg_size
    print(f"Number of bits required to represent the address is {add_size}")
    print(f"Number of bits available for opcode is {op_size}")
    print(f"Number of filler bits required for intruction of type - B is {inst_size - 2*reg_size - op_size}")
    print(f"Number of instructions supported by ISA is {(1<<op_size)}")
    print(f"Number of registers supported by the ISA is {(1<<reg_size)}")    
    return

def second_ques()->None:
    """Function to handle second question"""
    return

def main()->None:
    """Main Function to run the program"""
    print('Please enter the total memory of the system: ')
    mem_size = inpt_mem()
    if mem_size == -1:
        return
    add_type = inpt_add_type()
    if add_type == 'Invalid':
        return
    menu = ['Ques1 - ISA and length of instructions', 'Ques2 - System enhancement']
    print('Please enter the number of questions to process')
    itr = inpt_int()
    if(itr == -1):
        return
    for _ in range(itr):
        for cnt, option in enumerate(menu):
            print(f"{cnt}: {option}")
        print('Enter an appropriate choice: ')
        chosen = inpt_option(len(menu))
        if chosen == -1:
            return
        elif chosen == 1:
            first_ques()
        else:
            second_ques()
    return

if __name__ == '__main__':
    main()
else:
    raise Exception('The file cannot be imported')
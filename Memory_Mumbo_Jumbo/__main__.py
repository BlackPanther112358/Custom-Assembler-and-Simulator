import platform

nibble_size: int = 4
byte_size: int = 8
word_size: int = int(platform.architecture()[0][:-3])

conversions: dict = {'':0, 'k':10, 'M':20, 'G':30, 'T':40, 'P':50, 'E':60}

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
            inpt = int(input('Enter an option: '))
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
            pre = unit[0]
            if pre in conversions:
                unit = unit[1::]
            else:
                pre = ''
            val *= pow(2, conversions[pre])
            if (unit == 'b') or (unit.lower() == 'bit'):
                pass
            elif (unit == 'B') or (unit.lower() == 'byte'):
                val *= 8
            elif unit.lower() == 'word':
                val *= word_size
            elif unit.lower() == 'nibble':
                val *= 4
            else:
                print('Invalid unit entered')
                continue
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

def calculate_add_size(mem_size:int, curr_add_type:str, word_size:int = word_size)->int:
    """Calculates the address pins required to represent the memory"""
    add_cnt: int = mem_size
    match curr_add_type:
        case 'byte':
            add_cnt = (add_cnt + byte_size - 1)//byte_size
        case 'nibble':
            add_cnt = (add_cnt + nibble_size - 1)//nibble_size
        case 'word':
            add_cnt = (add_cnt + word_size - 1)//word_size
    add_size: int = 0
    while((1<<add_size) < add_cnt):
        add_size += 1
    return add_size

def first_ques(mem_size:int, add_type:str)->None:
    """Function to handle first question"""
    inst_size = inpt_int()
    if inst_size == -1:
        return
    reg_size = inpt_int()
    if reg_size == -1:
        return
    add_size = calculate_add_size(mem_size, add_type)
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

def second_ques(mem_size:int, add_type:str)->None:
    """Function to handle second question"""
    print('Please enter whether the query is of type 1 or type 2:')
    query_type: int = inpt_option(2)
    if query_type == -1:
        return
    elif query_type == 1:
        print('Enter how many bits CPU is: ')
        word_size = inpt_int()
        if word_size == -1:
            return
        new_add_type = inpt_add_type()
        if new_add_type == 'Invalid':
            return
        old_add_type:str = add_type
        old_add_size:int = calculate_add_size(mem_size, old_add_type, word_size)
        new_add_size:int = calculate_add_size(mem_size, new_add_type, word_size)
        print(f"The change in the number of address pins required is {new_add_size - old_add_size}")
    else:
        print('Enter how many bits CPU is: ')
        word_size = inpt_int()
        if word_size == -1:
            return
        word_pins:int = 0
        while (1<<word_pins) < word_size:
            word_pins += 1
        print('Please enter the number of address pins: ')
        add_pins:int = inpt_int()
        if add_pins == -1:
            return
        print('Please enter type of addressable memory: ')
        curr_add_type = inpt_add_type()
        if curr_add_type == 'Invalid':
            return
        match curr_add_type:
            case 'byte':
                add_pins += 3
            case 'nibble':
                add_pins += 2
            case 'word':
                add_pins += word_pins
        if add_pins < 3:
            print()
            print(f'Total output is {(1<<add_pins)} bits')
        else:
            add_pins -= 3
            suffix:str = 'B'
            convert_arr:list[int, str] = sorted([[conversions[key], key] for key in conversions.keys()], reverse=True)
            itr:int = 0
            while add_pins < convert_arr[itr][0]: 
                itr += 1
            add_pins -= convert_arr[itr][0]
            suffix = convert_arr[itr][1] + suffix
            print()
            print(f"The total memory available is {(1<<add_pins)} {suffix}")
    print()
    return

def main()->None:
    """Main Function to run the program"""
    print('Please enter the total memory of the system: ')
    mem_size:int = inpt_mem()
    if mem_size == -1:
        return
    add_type:str = inpt_add_type()
    if add_type == 'Invalid':
        return
    menu = ['Ques1 - ISA and length of instructions', 'Ques2 - System enhancement']
    print('Please enter the number of questions to process')
    itr = inpt_int()
    if(itr == -1):
        return
    for _ in range(itr):
        for cnt, option in enumerate(menu):
            print(f"{cnt + 1}: {option}")
        print('Enter an appropriate choice: ')
        chosen = inpt_option(len(menu))
        if chosen == -1:
            return
        elif chosen == 1:
            first_ques(mem_size, add_type)
        else:
            second_ques(mem_size, add_type)
    return

if __name__ == '__main__':
    main()
else:
    raise Exception('The file cannot be imported')
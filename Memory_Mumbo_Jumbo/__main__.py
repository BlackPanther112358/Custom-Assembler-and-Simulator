import platform

word_size = int(platform.architecture()[0][:-3])
conversions = {'':0, 'da':1, 'h':2, 'k':3, 'M':6, 'G':9, 'T':12, 'P':15, 'E':18}

def inpt_mem()->int:
    try_cnt = 0
    while(try_cnt < 3):
        try_cnt += 1
        try:
            inpt = input('Please enter the size of memory: ')
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

def first_ques()->None:
    return

def second_ques()->None:
    return
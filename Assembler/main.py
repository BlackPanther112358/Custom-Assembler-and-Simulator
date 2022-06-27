def take_input()->str:
    return

def convert(inpt:str)->str:
    return 

def output(ans:str):
    return

def main():
    ans = []
    while True:
        inpt = take_input()
        if inpt is False:
            raise Exception("Error")
        bitcode = convert(inpt)
        ans.append(bitcode)
        if inpt == 'hlt':
            break
    output(ans)

if '__name__' == '__main__':
    main()

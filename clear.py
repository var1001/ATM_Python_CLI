import os

def clear():
 
    # for windows
    if os.name == 'posix':
        _ = os.system('clear')
    else:
        _ = os.system('cls')
import os
import time

while True:
    os.system('clear')
    print("##############################")
    print("#          MAIN MENU         #")
    print("##############################")
    print()
    print("Select an action:")
    print("1. Rebuild databases")
    print("q. Quit")
    ans = input("> ")
    if (ans == '1'):
        import scrape
        time.sleep(5)
    elif (ans == 'q'):
        exit(0)
    else:
        print("Unrecognized option")
        time.sleep(5)

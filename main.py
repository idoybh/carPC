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
    print("2. Display data")
    print("3. Machine Learning")
    print("q. Quit")
    ans = input("> ")
    if (ans == '1'):
        exec(open("scrape.py").read())
        time.sleep(5)
    elif (ans == '2'):
        exec(open("data.py").read())
        import data
    elif (ans == '3'):
        exec(open("ML.py").read())
    elif (ans == 'q'):
        exit(0)
    else:
        print("Unrecognized option")
        time.sleep(3)

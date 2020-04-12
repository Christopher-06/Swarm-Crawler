import dbmanager
import swarmmanager
from threading import Thread
import time

def main():
    dbmanager.init()
    swarmmanager.swarm_start()   

    time.sleep(1)
    print("-----------------------")
    print("Ready to work")
    while True:
        INPUT = input()

        if INPUT == 'exit' or INPUT == 'break':
            print("-----------------------")
            print("Closing...")
            break

    #ending
    swarmmanager.swarm_stop()

if __name__ == "__main__":
    main()
import dbmanager
import swarmmanager
from threading import Thread
import time

swarmThread = None

def main():
    dbmanager.init()
    swarmThread = Thread(target=swarmmanager.swarm_run)
    swarmThread.daemon = True
    swarmThread.start()

    print("Ready to work")
    while True:
        INPUT = input()

        if INPUT == 'exit' or INPUT == 'break':
            print("Closing...")
            break

if __name__ == "__main__":
    main()
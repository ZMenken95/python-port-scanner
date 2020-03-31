""" imports required modules. Socket is used for the port scanner. Threading and Queue are used to "thread" the port scanners
 and create "jobs" in the queue. Logging is to create the log and time is to record the time the scan took. """
import socket
import threading
from queue import Queue
import logging
import time

# defines our log, what we need it to log
logging.basicConfig(filename="zscan.log", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")

# the '.lock' function prevents more than one worker using a function, in this case print, simultaneously.
print_lock = threading.Lock()

# ask the user to input the target server.
server = input("enter a host to scan \n")
start = time.time()

# Simply for look, makes the log file easier to read
logging.info("The following log displays the target host plus detected open ports:")
logging.info(server)

# simply for look during the scan
print("Scanning ", server, "...............")

logging.info("The following ports were discovered open:")

# this defines our port scanner. A connection attemt will be made. If successful, the script will print and log the open
# port. We need the "print_lock" function to prevent 2 workers from printing simultaneously.
def zscan(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        con = s.connect((server, port))
        with print_lock:
            print("port", port, "is open!")
            logging.info(port)
        con.close()
    # Tries to account for any conceivable error. If the URL/IP was invalid the system will warn the user.
    # Other errors are connection errors, we want them to pass gracefully.
    except socket.gaierror:
        print("Invalid address, pls quit and rerun with a valid URL or IP")
    except TimeoutError:
        pass
    except ConnectionRefusedError:
        pass
    except AttributeError:
        pass
    except OSError:
        pass


# This defines our threader, it gets the "workers" assigns their job and has them complete so worker can be used for
# an additional job.
def threader():
    while True:
        worker = q.get()
        zscan(worker)
        q.task_done()

# Defines the queue
q = Queue()

# Now the process is ready to begin. The threader will get 100 workers. Daemon = true will "kill" the workers once the
# entire task is complete as they are no longer needed. Once that is defined they can start.
for x in range(100):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

# How many jobs are needed. We have 1025 ports to be scanned.
for worker in range(1, 1026):
    q.put(worker)

# Workers join the queue and receive their job.
q.join()

# Look and feel of the log.
logging.info("Scan completed")

# Ends the process timer and coverts into hours,minutes,seconds to make the clock user readable. This info
# is then printed and logged.
end = time.time()
temp = end-start
hours = temp//3600
temp = temp - 3600*hours
minutes = temp//60
seconds = temp - 60*minutes
print('The scan took: %d:%d:%d' %(hours,minutes,seconds))
logging.info('The scan took: %d:%d:%d' %(hours,minutes,seconds))
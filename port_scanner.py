import socket
import threading
import time
from queue import Queue

# Target IP (use your local machine or a test server)
target = "127.0.0.1"  # Change to "scanme.nmap.org" for public test
port_range = range(1, 1025)  # Common ports
open_ports = []

# Function to scan a single port
def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((target, port))
    if result == 0:
        open_ports.append(port)
    sock.close()

# Threading worker
def worker(queue):
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

# Main scanner function
def run_scanner():
    start_time = time.time()
    queue = Queue()
    
    for port in port_range:
        queue.put(port)
    
    threads = []
    for _ in range(50):
        thread = threading.Thread(target=worker, args=(queue,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"Scan finish for {target} in {end_time - start_time:.2f} seconds")
    if open_ports:
        print(f"Ports wey dey open for {target}: {sorted(open_ports)}")
        for port in open_ports:
            try:
                service = socket.getservbyport(port, "tcp")
            except OSError:
                service = "Unknown"
            print(f"Port {port} dey open - E fit be {service}")
    else:
        print(f"No port dey open for {target}—e tight o!")

if __name__ == "__main__":
    print(f"Scanning {target}—make we see wetin dey...")
    run_scanner()
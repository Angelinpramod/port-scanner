import socket
import threading
from queue import Queue

COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    631: "CUPS",
    9050: "TOR SOCKS"
}

target = input("Enter target (IP or domain): ")
ip = socket.gethostbyname(target)

queue = Queue()
results = []
lock = threading.Lock()

def scan(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)

            result = s.connect_ex((ip, port))

            if result == 0:
                service = COMMON_SERVICES.get(port, "Unknown")

                banner = "No banner"

                # Protocol-aware logic
                if port in [80, 8080, 8000, 631]:
                    try:
                        s.send(b"GET / HTTP/1.1\r\nHost: test\r\n\r\n")
                        banner = s.recv(1024).decode(errors="ignore").split("\n")[0]
                    except:
                        pass
                else:
                    try:
                        banner = s.recv(1024).decode(errors="ignore").strip()
                    except:
                        pass

                with lock:
                    results.append((port, service, banner))

    except:
        pass

def worker():
    while True:
        try:
            port = queue.get_nowait()
        except:
            break

        scan(port)
        queue.task_done()


for port in range(1, 1000):
    queue.put(port)

# Threads
for _ in range(50):
    t = threading.Thread(target=worker)
    t.start()

queue.join()

print("\nOpen Ports & Services:\n")
for port, service, banner in sorted(results):
    print(f"[OPEN] {port} → {service} → {banner}")


print(f"\nTotal Open Ports: {len(results)}")

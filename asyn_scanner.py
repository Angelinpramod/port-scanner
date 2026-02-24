import asyncio
import time
#service names for common ports
SERVICE_NAMES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    631: "CUPS",        
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Proxy",
    8443: "HTTPS-Alt",
}
# Connect to a port and attempt to grab a banner if open
async def scan_port(ip, port, sem):
    async with sem:
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port), timeout=0.1
            )
            banner = await banner_grab(reader, writer, ip, port)
            writer.close()
            await writer.wait_closed()
            service = SERVICE_NAMES.get(port, "Unknown") 
            if banner:
                print(f"[+] Port {port} ({service}) → {banner}")
            else:
                print(f"[+] Port {port} ({service})")
        except asyncio.TimeoutError:
            pass
        except ConnectionRefusedError:
            pass
        except OSError:
            pass
        except Exception as e:
            print(f"[!] Unexpected error on port {port}: {e}")
#Banner grabbing logic based on port number, with timeouts and error handling
async def banner_grab(reader, writer, ip, port):
    try:
        if port in [80, 8080, 8000, 8443, 631]:
            writer.write(b"GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n")
            await writer.drain()
        data = await asyncio.wait_for(reader.read(1024), timeout=1.0)
        if data:
            first_line = data.decode(errors="ignore").splitlines()[0].strip()
            return first_line[:80]  
    except asyncio.TimeoutError:
        pass
    except OSError:
        pass
    return ""
#main function
async def main():
    ip = input("Enter IP: ")
    sem = asyncio.Semaphore(200)
    tasks = [scan_port(ip, i, sem) for i in range(1, 1025)]
    await asyncio.gather(*tasks)

start_time = time.time()
asyncio.run(main())
elapsed = time.time() - start_time
print(f"Scan completed in {elapsed:.2f} seconds")

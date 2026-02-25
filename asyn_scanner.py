import asyncio
import time

SERVICE_NAMES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 631: "CUPS",
    3306: "MySQL", 3389: "RDP", 8080: "HTTP-Proxy",
    8443: "HTTPS-Alt",
}

TOP_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 139, 143,
    443, 445, 3306, 3389, 8080, 8443, 20,
    137, 138, 389, 636
]

CVE_DB = {
    "Apache/2.4.49": "CVE-2021-41773",
    "OpenSSH_7.2": "CVE-2016-0777",
    "vsFTPd 2.3.4": "Backdoor Vulnerability"
}

scanned = 0
total = 0
lock = asyncio.Lock()

async def banner_grab(reader, writer, ip, port):
    try:
        if port in [80, 8080, 8000, 8443, 631]:
            writer.write(f"GET / HTTP/1.1\r\nHost: {ip}\r\nConnection: close\r\n\r\n".encode())
            await writer.drain()

        data = await asyncio.wait_for(reader.read(1024), timeout=1.0)

        if data:
            return data.decode(errors="ignore").splitlines()[0][:80]

    except:
        pass

    return ""

async def scan_port(ip, port, sem):
    global scanned

    async with sem:
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(ip, port), timeout=0.2
            )

            banner = await banner_grab(reader, writer, ip, port)
            writer.close()
            await writer.wait_closed()

            service = SERVICE_NAMES.get(port, "Unknown")

            vuln = ""
            for key in CVE_DB:
                if key in banner:
                    vuln = f"{CVE_DB[key]}"

            if banner:
                print(f"\n[+] Port {port} ({service}) → {banner}{vuln}")
            else:
                print(f"\n[+] Port {port} ({service})")

        except:
            pass

        async with lock:
            scanned += 1
            print(f"\rProgress: {scanned}/{total}", end="")

async def main():
    global total

    ip = input("Enter target IP: ")
    mode = input("Scan top ports only? (y/n): ").lower()

    ports = TOP_PORTS if mode == "y" else range(1, 1025)
    total = len(ports)

    sem = asyncio.Semaphore(200)

    tasks = [scan_port(ip, p, sem) for p in ports]
    await asyncio.gather(*tasks)

start = time.time()
asyncio.run(main())
print(f"\nScan completed in {time.time() - start:.2f} seconds")

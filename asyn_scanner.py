import asyncio
sem=asyncio.Semaphore(100)
async def scan_port(ip,port):
    async with sem:
        try:
            reader, writer = await asyncio.open_connection(ip, port)
            print(f"Port {port} is open")
            if port in [80,8000,8080]:
                writer.write(b"GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
                await writer.drain()
                data=await reader.read(1024)
                print(f"Banner {port}: {data.decode(errors='ignore').splitlines()[0] if data else 'No banner'}")
            writer.close()
            await writer.wait_closed()

        except Exception:
            pass
async def main():
    ip=input("Enter IP address to scan: ")
    tasks=[scan_port(ip, port) for port in range(1, 1025)]
    await asyncio.gather(*tasks)
asyncio.run(main())   
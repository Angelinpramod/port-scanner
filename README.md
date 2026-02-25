# 🚀 Python Port Scanner (Learning Project)

This project demonstrates the **evolution of a port scanner** from a basic implementation to an advanced async-based tool.

This is just me learning and trying to understand things like:

* Networking basics
* Port scanning
* Concurrency (Threads vs Async)
* Banner grabbing
* Basic vulnerability awareness

---

# 📂 Project Structure

```
port-scanner/
│
├── basic_scanner.py      # 🥇 v1 - Basic scanner (single-threaded)
├── scanner.py            # 🥈 v2 - Multithreaded scanner
├── asyn_scanner.py       # 🥉 v3 - Async scanner with CVE hints
├── README.md
```

---

# 🧠 Versions Explained

## 🥇 v1 - Basic Scanner (`basic_scanner.py`)

* Uses Python `socket`
* Scans ports sequentially
* Detects open ports using `connect_ex()`

👉 Good for understanding fundamentals

---

## 🥈 v2 - Multithreaded Scanner (`scanner.py`)

* Uses `threading` and `Queue`
* Faster scanning with concurrency
* Basic banner grabbing
* Thread-safe using locks

👉 Introduces real-world performance concepts

---

## 🥉 v3 - Async Scanner (`asyn_scanner.py`)

* Uses `asyncio` (event-driven concurrency)
* High-performance scanning ⚡
* Banner grabbing
* Service detection
* CVE hinting (basic)
* Progress tracking

👉 Closest to real-world tools like Nmap (conceptually)


---

# 🧪 Example Usage

```
Enter target IP: 127.0.0.1
Scan top ports only? (y/n): y
```

Output:

```
[+] Port 80 (HTTP) → HTTP/1.1 200 OK
[+] Port 22 (SSH)
Progress: 20/20
```

---

# ⚠️ Disclaimer

This tool is created for:

* Educational purposes
* Learning cybersecurity concepts

❗ Do NOT scan systems without permission.

---

# 📈 What I Learned

* TCP socket programming
* Difference between blocking vs non-blocking I/O
* Multithreading vs Async programming
* Banner grabbing techniques
* Basic vulnerability mapping

---

# 👨‍💻 Author

**Angelin Pramod**
Cybersecurity learner | CTF enthusiast

---

# ⭐ If you found this useful

Give it a star ⭐ and feel free to contribute!
